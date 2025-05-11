import requests
import base64
from io import BytesIO
from PIL import Image
import json
import socket
import time
import bfl_finetune

def get_model_endpoint(model_id: str) -> str:
    """
    Get the correct API endpoint for the given model
    """
    endpoints = {
        "flux-pro": "https://api.us1.bfl.ai/v1/flux-pro",
        "flux-pro-1.1": "https://api.us1.bfl.ai/v1/flux-pro-1.1",
        "flux-pro-1.1-ultra": "https://api.us1.bfl.ai/v1/flux-pro-1.1-ultra",
        "flux-pro-finetuned": "https://api.us1.bfl.ai/v1/flux-pro-finetuned"
    }
    return endpoints.get(model_id, "https://api.us1.bfl.ai/v1/flux-pro-1.1")  # Default to flux-pro-1.1 if model not found

def test_dns_resolution(hostname: str) -> bool:
    """
    Test if a hostname can be resolved
    """
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False

def poll_for_result(api_key: str, task_id: str, max_attempts: int = 30, delay: float = 2.0) -> dict:
    """
    Poll the API for the result of a task
    """
    headers = {
        "x-key": api_key.strip(),
        "Accept": "application/json"
    }
    
    polling_url = f"https://api.us1.bfl.ai/v1/get_result?id={task_id}"
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(polling_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # Print debug information
            print(f"Polling attempt {attempt + 1}/{max_attempts}")
            print(f"Response status: {response.status_code}")
            print(f"Response content: {result}")
            
            if result.get("status") == "Ready":
                return result
            elif result.get("status") in ["Error", "Request Moderated", "Content Moderated"]:
                raise Exception(f"Task failed with status: {result.get('status')}")
                
            time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Polling request failed: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse polling response")
            
    raise Exception("Max polling attempts reached")

def download_image(url: str) -> Image.Image:
    """
    Download an image from a URL and return it as a PIL Image
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        raise Exception(f"Failed to download image: {str(e)}")

def generate_image(
    api_key: str,
    model_id: str,
    prompt: str,
    width: int,
    height: int,
    steps: int,
    guidance_scale: float,
    seed: int = -1,
    image_prompt: str = None,
    finetune_id: str = None,
    finetune_strength: float = 1.0,
    use_raw_mode: bool = False,
    prompt_upsample: bool = True,
    interval: float = 2.0
) -> list:
    """
    Generate images using the BFL API
    Returns a list of PIL Image objects
    """
    headers = {
        "x-key": api_key.strip(),  # Use x-key header as per API spec
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Remove model from payload since it's in the URL
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "guidance_scale": guidance_scale,
        "seed": seed if seed != -1 else None,
        "prompt_upsampling": prompt_upsample,
        "interval": interval
    }

    if image_prompt:
        # Convert image to base64
        buffered = BytesIO()
        image_prompt.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        payload["image_prompt"] = img_str

    if finetune_id:
        payload["finetune_id"] = finetune_id
        payload["finetune_strength"] = finetune_strength

    if use_raw_mode:
        payload["raw"] = True  # Changed from raw_mode to raw as per API spec

    try:
        # Special handling for finetuned model
        if model_id == "flux-pro-finetuned":
            # Use bfl_finetune.finetune_inference for correct endpoint and polling
            resp = bfl_finetune.finetune_inference(
                finetune_id=finetune_id,
                finetune_strength=finetune_strength,
                api_key=api_key,
                prompt=prompt,
                width=width,
                height=height,
                steps=steps,
                guidance_scale=guidance_scale,
                seed=seed if seed != -1 else None,
                prompt_upsampling=prompt_upsample,
                interval=interval,
                raw=use_raw_mode
            )
            # The rest of the logic expects a task/result structure
            task_id = resp.get("id")
            if not task_id:
                raise Exception("No task ID received from API (finetuned)")
            result = poll_for_result(api_key, task_id)
            if "result" in result and "sample" in result["result"]:
                image_url = result["result"]["sample"]
                print(f"Downloading image from: {image_url}")
                image = download_image(image_url)
                return [image]
            else:
                print("No image URL found in result (finetuned)")
                print(f"Full result: {result}")
                return []
        # Default: base model logic
        endpoint = get_model_endpoint(model_id)
        hostname = endpoint.split("//")[1].split("/")[0]
        # Test DNS resolution
        if not test_dns_resolution(hostname):
            raise Exception(f"Could not resolve hostname: {hostname}. Please check your internet connection and DNS settings.")
        print(f"Making request to: {endpoint}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        response = requests.post(endpoint, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        task_response = response.json()
        task_id = task_response.get("id")
        if not task_id:
            raise Exception("No task ID received from API")
        result = poll_for_result(api_key, task_id)
        if "result" in result and "sample" in result["result"]:
            image_url = result["result"]["sample"]
            print(f"Downloading image from: {image_url}")
            image = download_image(image_url)
            return [image]
        else:
            print("No image URL found in result")
            print(f"Full result: {result}")
            return []
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Failed to parse API response")
    except Exception as e:
        raise Exception(f"Image generation failed: {str(e)}") 
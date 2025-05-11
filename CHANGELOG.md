# Changelog

## [Unreleased]
- Initial changelog created.

## [2024-05-10]
### Added
- Added robust error handling for all BFL API calls in both Finetuning and Inference tabs.
- Added a dedicated error display for finetune listing and selection.
- Added support for listing, selecting, and deleting finetunes from the UI.
- Added support for running inference with a selected finetune.
- Added "Flux1 Pro Finetune" to the model dropdown, using the correct `/v1/flux-pro-finetuned` endpoint.
- Added automatic mapping of UI values to BFL API values for priority and finetune type.
- Added clear user feedback for API errors and empty results.

### Changed
- Updated inference logic to use the correct endpoint and payload for finetuned models.
- Improved dropdown and table handling to support both string and dict API responses.
- Improved UI to prevent crashes when API returns errors or empty lists.

### Fixed
- Fixed bug where finetune IDs returned as strings would cause UI errors.
- Fixed bug where error messages would appear in dropdowns instead of dedicated error boxes.

---

For earlier changes, see project commit history. 
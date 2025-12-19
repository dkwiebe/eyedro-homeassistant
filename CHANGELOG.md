# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2024-12-19

### Added
- Options flow handler to allow configuration changes from Home Assistant UI
- Users can now configure scan interval settings through the integration's Configure button
- Automatic coordinator update when options are changed

### Changed
- Scan interval now reads from options first, then falls back to config entry data
- Improved configuration management with separate options flow

## [0.0.3] - 2024-12-19

### Changed
- No code changes - version bump for troubleshooting and verification

## [0.0.2] - 2024-12-19

### Changed
- Enhanced config flow with improved validation and error handling
- Added IP address format validation in config flow
- Improved UI strings with better descriptions and field labels
- Enhanced error messages with more helpful guidance
- Added input sanitization (trimming whitespace from host address)

### Fixed
- Improved error handling for invalid IP addresses with field-specific error messages

## [0.0.1] - 2024-12-19

### Added
- Initial release of Eyedro Home Assistant integration
- Config flow for UI-based setup (IP address, port, scan interval)
- Four sensor entities:
  - Total Power (kW)
  - Total Current (A)
  - Average Voltage (V)
  - Average Power Factor (%)
- Data coordinator for efficient API polling
- API client for Eyedro EYEFI device communication
- Test script (`test_eyedro_api.py`) to validate API response format
- HACS compatibility with `hacs.json`
- README with installation and usage instructions
- MIT License

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)


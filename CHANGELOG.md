# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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


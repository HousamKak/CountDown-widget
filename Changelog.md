# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-04-30
### Added
- **Session Naming:** Ability to assign a custom name to each countdown session.
- **Real‑Time Analytics:** Live display of active vs. paused durations during a session.
- **History View:** A collapsible tree table listing past sessions with columns: Name, Start, Length, Active, Paused.
- **Clear History:** One‑click button to remove all recorded sessions.

### Changed
- **Layout Refactor:** Flexible packing and responsive sizing; improved padding and color scheme.
- **UI Components:** Switched to `ttk.Treeview` for history; updated button styling and hover effects.

### Fixed
- Guard against duplicate session recordings on reset or timer completion.
- Prevent multiple concurrent countdown callbacks.
- Minor bug fixes and performance optimizations.

## [1.0.0]
### Added
- Basic countdown functionality supporting hours, minutes, or seconds.
- **START**, **PAUSE**, **RESET** controls with state transitions.
- Display of remaining time in `HH:MM:SS` format and a `TIME'S UP!` message at completion.
- Prevention of overlapping countdowns and restart capability.

*For earlier releases, please refer to the project’s Git history.*


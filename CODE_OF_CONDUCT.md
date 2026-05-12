# Code of Conduct

## Our Pledge

We as contributors and maintainers of the **YOLO11 Inference Microservice** pledge to make participation in this project a respectful, inclusive, and harassment-free experience for everyone — regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

We are committed to building a welcoming environment where contributors at all skill levels — from those new to FastAPI and computer vision to seasoned ML engineers — can collaborate effectively.

---

## Our Standards

### Expected Behavior

- **Be respectful and constructive.** Critique ideas, not people. Code reviews and issue discussions should focus on improving the project.
- **Be inclusive.** Welcome contributors regardless of their background or experience with YOLO, PyTorch, or FastAPI.
- **Be collaborative.** Share knowledge openly — whether it's about model optimization, hardware configuration (CUDA vs. CPU), or API design patterns.
- **Be transparent.** Clearly document your changes, especially around model behavior, inference logic, or breaking API changes (e.g., modifications to `/api/v1/detect` or `/api/v1/health`).
- **Be patient.** ML environments can be complex to set up. Help others debug dependency or hardware issues rather than dismissing them.

### Unacceptable Behavior

- Harassment, insults, or derogatory comments in any project space (issues, pull requests, discussions, commits).
- Deliberate introduction of regressions, malicious code, or backdoors — especially concerning inference logic, model weights in `models/`, or security-sensitive components in `app/core/`.
- Dismissing contributors for using CPU instead of GPU, or for preferring `pip` over `uv`.
- Spamming issues or pull requests with off-topic or low-effort content.
- Publishing others' private information without explicit permission.

---

## Contribution Guidelines

To keep the codebase healthy and consistent:

- **Follow the project structure.** New logic belongs in the appropriate layer — routes in `app/api/`, business logic in `app/services/`, schemas in `app/models/`, and configuration in `app/core/`.
- **Respect versioning.** New endpoints must be placed under `/api/v1/`. Do not modify legacy root endpoints (`/health`, `/detect`) without prior discussion — they are maintained for backward compatibility.
- **Test before submitting.** Use `test_service.py` to verify inference behavior. Provide evidence of testing in your pull request.
- **Document your changes.** If your contribution affects the `footage-hub` integration, the `.env` configuration (`YOLO_SERVICE_URL`), or the Docker setup, update the relevant documentation.
- **Hardware considerations.** Contributions should function on both CUDA and CPU environments. Do not assume GPU availability.

---

## Reporting Issues

If you experience or witness unacceptable behavior, please report it by opening a private issue or contacting the maintainers directly. All reports will be reviewed and investigated promptly and confidentially.

When reporting a **security vulnerability** (e.g., in the API, model loading, or inference pipeline), please do **not** open a public issue. Contact the maintainers privately so it can be addressed before disclosure.

---

## Enforcement

Project maintainers are responsible for clarifying and enforcing this Code of Conduct. They have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that do not align with this Code of Conduct, and to temporarily or permanently ban contributors for behaviors they deem inappropriate, threatening, or harmful.

---

## Scope

This Code of Conduct applies to all project spaces — GitHub issues, pull requests, discussions, and any other channels used by the project community. It also applies when an individual is officially representing the project in public spaces.

---

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org/), version 2.1, and tailored to the specific context of the YOLO11 Inference Microservice project.
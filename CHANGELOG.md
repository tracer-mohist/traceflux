# CHANGELOG

<!-- version list -->

## v1.2.1 (2026-03-11)

### Bug Fixes

- Add black/isort/flake8 to dev dependencies
  ([`56c70a2`](https://github.com/tracer-mohist/traceflux/commit/56c70a2b7418206aa24d27c19107383e36286135))

### Chores

- Fix root documentation quality issues
  ([`d232a09`](https://github.com/tracer-mohist/traceflux/commit/d232a09c4a8d3d7a0e1fe8ab745a91a02b91e149))

- Remove obsolete template + add markdown emphasis check
  ([`0c41a40`](https://github.com/tracer-mohist/traceflux/commit/0c41a407ecfcbae3a9ba8c8f9e94594ffcdb713c))

- Restructure docs with layered architecture
  ([`1da9330`](https://github.com/tracer-mohist/traceflux/commit/1da9330839d0131156a616facbf167bc52c80e73))

- **config**: Add gitlint for commit message validation
  ([`425a881`](https://github.com/tracer-mohist/traceflux/commit/425a881d087c4c95fcede2175fce9acfb27da4f7))

- **config**: Configure gitlint to ignore body length checks
  ([`30e1d43`](https://github.com/tracer-mohist/traceflux/commit/30e1d43370c6bafd670a3e7d20e98ad9abc9b85d))

- **release**: Fix changelog auto-update configuration
  ([`b68acfc`](https://github.com/tracer-mohist/traceflux/commit/b68acfcb2db2f43908bdc1cdc115bf96219620a3))

### Continuous Integration

- Cache .venv instead of ~/.cache/pdm
  ([`b4baf46`](https://github.com/tracer-mohist/traceflux/commit/b4baf46b180e5699b0595d12b105ad9a3d55bd42))

- Complete documentation quality checker ([#40](https://github.com/tracer-mohist/traceflux/pull/40),
  [`e18d47a`](https://github.com/tracer-mohist/traceflux/commit/e18d47a19f5350b4b731a413d93c85481a4a64a9))

- Consolidate workflows and add caching
  ([`4ed13b0`](https://github.com/tracer-mohist/traceflux/commit/4ed13b0b280c1668c5b9ae11bef89f81a4f3c50f))

- Finalize docs quality checker
  ([`29c9bfe`](https://github.com/tracer-mohist/traceflux/commit/29c9bfe3e56e1d57720d6cfcb7f25ba50e8cdeeb))

- Fix check-docs-quality.py to match issue #40 spec
  ([`5512f79`](https://github.com/tracer-mohist/traceflux/commit/5512f79c640c871e858d12462dfdc986dbf98ab1))

- Fix dev dependency installation in workflows
  ([`c76da24`](https://github.com/tracer-mohist/traceflux/commit/c76da2457841b2b2ae533c29651dcc5b0b557802))

- Fix workflow design to avoid duplicate testing
  ([`6cb7af5`](https://github.com/tracer-mohist/traceflux/commit/6cb7af519a927260777f30ee56b691d5ab279bf5))

- Remove broken venv cache
  ([`ccf8824`](https://github.com/tracer-mohist/traceflux/commit/ccf88240991781b51c65761b732a01a962efbf10))

- Simplify CD and remove low-value test
  ([`9e29adc`](https://github.com/tracer-mohist/traceflux/commit/9e29adc7105ff1743b3e2845389ef67f560d6e08))

- Simplify test workflow and fix dependency install
  ([`ce33f53`](https://github.com/tracer-mohist/traceflux/commit/ce33f5340b34116fa6675d3d2c896f9c9b0f917c))

- Trigger CI on push to main for safety
  ([`b77011e`](https://github.com/tracer-mohist/traceflux/commit/b77011eac2123372d55cb59550369b8bd09ffb7b))

- Update docs quality config: ignore .pytest_cache/ and .github/
  ([`19ad22c`](https://github.com/tracer-mohist/traceflux/commit/19ad22c0f837f54d90cc9b2a0026c7b0b1a34fd5))

### Documentation

- Complete restructuring, remove research/ and drafts/
  ([`3fa1581`](https://github.com/tracer-mohist/traceflux/commit/3fa15813a01e08316662e945501f8a7db75b8ab6))

- Fix associations documentation quality
  ([`237b024`](https://github.com/tracer-mohist/traceflux/commit/237b024703e93ad8df69eb39d8c7bbf7548a00ac))

- Fix documentation quality issues
  ([`61a0f0d`](https://github.com/tracer-mohist/traceflux/commit/61a0f0dc310c41813655bf616c3abd3c1b186acb))

- Fix foundations documentation quality
  ([`59a5ad8`](https://github.com/tracer-mohist/traceflux/commit/59a5ad8926becd83c28fae92c9caef884b694372))

- Fix philosophy documentation quality
  ([`33fd0a9`](https://github.com/tracer-mohist/traceflux/commit/33fd0a9be39c7a1c4c074862516a319d1926baa9))

- Fix quality issues - split large files, remove ** and non-ASCII
  ([`6b6437a`](https://github.com/tracer-mohist/traceflux/commit/6b6437a27872776d4963c94c5b15817efc9c284e))

- Fix root documentation quality
  ([`c1dd2d0`](https://github.com/tracer-mohist/traceflux/commit/c1dd2d0107bf569d03d70523993d41684a4b7789))

- Restructure research materials into organized docs
  ([`60ac7cc`](https://github.com/tracer-mohist/traceflux/commit/60ac7ccf24cbe76e33e17548b9b5d6105b7fd925))

- Rewrite CHANGELOG.md for semantic-release automation
  ([`6ef04f4`](https://github.com/tracer-mohist/traceflux/commit/6ef04f44b1d555f8ad1c224b8bc1b615300723bd))

### Testing

- Fix version assertion to work with semantic-release
  ([`7024fa9`](https://github.com/tracer-mohist/traceflux/commit/7024fa99200738ae08ec9d4c29486e6af6809a8f))


## v1.2.0 (2026-03-10)

### Chores

- Complete Phase 8 infrastructure setup
- Update todo.md, remove intermediate TODO file

### Continuous Integration

- Add new workflow files (pr-check, test, cd)
- Delete old ci.yml (replaced by pr-check, test, cd)

### Documentation

- Add branch protection analysis
- Add GitHub branch protection research
- Add Phase 8 status report
- Documentation cleanup and restructuring
- Reduce README to 80 lines, extract details to docs/
- Update RELEASE_PROTOCOL.md for automated workflow
- release: Update guide for semantic-release workflow

### Features

- release: Automate versioning with pdm + semantic-release

## v1.1.0 (2026-03-07)

### Features

- Core search functionality
- Associative keyword extraction
- PageRank-based suggestion engine
- UNIX pipe support (stdin/stdout)

### Documentation

- Comprehensive documentation (README, PHILOSOPHY, examples)

### Testing

- Test suite (174+ tests)

## v1.0.0 (2026-03-07)

### Added

- Initial release

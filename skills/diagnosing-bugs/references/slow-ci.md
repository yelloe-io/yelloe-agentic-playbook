# Slow or costly CI

Use this when a CI run is slow or uses too many billed minutes. Do the steps in this order. Do not change the CI before step 1. The examples use GitHub Actions and pytest. Use the equivalent tools of your stack.

1. **Measure the runner.** Add a probe job that runs `nproc`, `lscpu` and `free -g`. On GitHub, `ubuntu-latest` can show 2 CPUs with only 1 physical core. Parallel workers do not help on 1 core.
2. **Find the slow step.** Run `gh run view <id> --json jobs` and compare the `startedAt` and `completedAt` of each step. For a slow test step, run `pytest --durations=12` locally. One slow test needs a fix in that test. Many small tests need a shorter run.
3. **Take the free wins.**
   - Cancel stale runs: `concurrency` with `cancel-in-progress: true`, keyed on the branch.
   - Set `timeout-minutes` on each job.
   - Run a small job, such as a path filter, on a cheap runner such as `ubuntu-slim`.
   - Run an expensive test setup once per session, not once per test or file. Cache it in `conftest.py` and return copies.
4. **Skip jobs that do not apply.** Use `dorny/paths-filter` so that a pull request runs only the jobs for the folders it changes. A push to `main` runs all jobs. The filter job needs `permissions: contents: read, pull-requests: read`. Without it, the job fails with "Resource not accessible by integration".
5. **Paid options last.** Shards across jobs, larger runners and parallel workers cost money or setup time. Show the user a table of the billed minutes added against the minutes saved, and let the user decide.
   - With more than 1 core, use `pytest -n auto --dist loadfile` and set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS` and `MKL_NUM_THREADS` to 1.
   - On 1 core, shard the test files across a job matrix. Time each shard locally, and check that the shard test counts add up to the full count. Each shard adds about 1 minute of runner setup.
6. **Measure on the runner, twice.** A local speed-up proves nothing about the runner. The same run can change by 2 minutes on one day.

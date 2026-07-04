# Nayarit CNN Challenge Submissions

This repository receives student submissions for the CNN image classification
leaderboard challenge. Students do not push directly to this repository.
Instead, each student opens a GitHub Issue with the `Model submission` form and
uploads one ZIP file:

- `submission.zip`

The ZIP must contain:

- `predictions.csv`
- `ABLATIONS.md`

The workflow validates each submission, evaluates it against hidden test labels,
archives the student's latest valid attempt, and updates the leaderboard.

## Student Workflow

1. Train your model in the main challenge repository.
2. Generate `predictions.csv` with exactly these columns:

   ```csv
   id,y_pred
   test_000001,0
   test_000002,3
   test_000003,4
   ```

3. Write `ABLATIONS.md` describing ablations or experiments.
4. Create `submission.zip` containing `predictions.csv` and `ABLATIONS.md`.
5. Open a new issue in this repository using the `Model submission` form.
6. Upload `submission.zip` in the form.
7. Submit the form.
8. Wait for the GitHub Actions confirmation comment.

## Required Issue Form Fields

- `student_id`
- `student_name`
- `model_name`
- `num_parameters`
- `validation_accuracy`
- `validation_f1_macro`
- `submission_zip`

The optional field is `notes`.

## File Validation

`predictions.csv` must contain exactly two columns, in this order:

```csv
id,y_pred
```

Validation rules:

- No missing IDs.
- No duplicated IDs.
- No missing predictions.
- `y_pred` must be an integer.
- `y_pred` must be between `0` and `4`.
- No extra columns are allowed.

`ABLATIONS.md` validation rules:

- The file must exist.
- The file must not be empty.
- The file should contain one of these words: `Ablation`, `ablation`,
  `Experiment`, or `experiment`.

The workflow never executes student code and never installs student
dependencies.

## Hidden Test Evaluation

The evaluator expects hidden labels at:

```text
data/private/test_labels.csv
```

The CSV must contain at least these columns:

```csv
id,label
```

It may contain extra instructor-only columns such as `filename` or `class_name`.

Do not commit hidden labels to a public or student-readable repository. The
recommended setup is:

1. Store the hidden labels in the private repository
   `alonso59/test_set_nayarit_challenge1`.
2. Put the file at the repository root:

   ```text
   test_labels.csv
   ```

3. Configure a repository secret named `TEST_LABELS_SSH_KEY` in this leaderboard
   repository. The secret must contain an SSH private key that can read
   `alonso59/test_set_nayarit_challenge1`.

Recommended GitHub setup:

1. Create a dedicated SSH key pair for the workflow:

   ```bash
   ssh-keygen -t ed25519 -C "nayarit-challenge-hidden-labels" -f ~/.ssh/nayarit_challenge_hidden_labels
   ```

2. In the private labels repository, add the public key as a read-only deploy
   key:

   ```text
   https://github.com/alonso59/test_set_nayarit_challenge1/settings/keys
   ```

   Use the contents of:

   ```text
   ~/.ssh/nayarit_challenge_hidden_labels.pub
   ```

3. In this leaderboard repository, open:

   ```text
   Settings -> Secrets and variables -> Actions -> New repository secret
   ```

4. Add:

   ```text
   TEST_LABELS_SSH_KEY=<contents of ~/.ssh/nayarit_challenge_hidden_labels>
   ```

With this secret configured, the workflow downloads the hidden labels on every
submission without instructor intervention. Students can submit through issues,
but they cannot see the hidden label file or key.

The workflow still supports an HTTPS fallback using `TEST_LABELS_CSV_URL` and
`TEST_LABELS_TOKEN`, but the SSH deploy key path is preferred for this challenge.

If this repository is private and students cannot read its contents, the
instructor may also place the file directly at `data/private/test_labels.csv`.
That file is ignored by `.gitignore` by default to reduce the risk of accidental
publication. If the instructor intentionally wants to version it in a private
evaluator repository, use `git add -f data/private/test_labels.csv` or remove
that ignore rule.

The workflow checks that submitted IDs match the hidden test IDs exactly. Missing
or unknown IDs cause rejection.

## Scoring

The workflow computes:

```text
final_score = 0.70 * macro_f1 + 0.20 * accuracy + 0.10 * efficiency_score
```

There is no maximum parameter limit. The current efficiency rule is:

```text
efficiency_score = min(1.0, 100000 / num_parameters)
```

This keeps `efficiency_score` in the range `[0, 1]`, gives full efficiency credit
to models with at most 100,000 parameters, and gradually penalizes larger models
without disqualifying them.

## Instructor Policy

Each `student_id` has only one visible latest submission. If a student submits
again, the files in `submissions/<student_id>/latest/` are overwritten.

All processed attempts that can be parsed are recorded in
`leaderboard/submissions_log.csv`. The public summary in
`leaderboard/latest_submissions.md` shows only the latest accepted submission per
student, ranked by `final_score`.

# Nayarit CNN Challenge Submissions

This repository receives student submissions for the CNN image classification
leaderboard challenge. Students do not push directly to this repository.
Instead, each team opens a GitHub Issue with the `Model submission` form and
provides direct download links for two files:

- `predictions.csv`
- `ABLATIONS.md`

This first version validates and archives submissions only. Hidden-label test
evaluation will be added later.

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
4. Push both files to your own repository or fork.
5. Copy the raw URL for each file. GitHub raw URLs usually begin with
   `https://raw.githubusercontent.com/...`.
6. Open a new issue in this repository using the `Model submission` form.
7. Submit the form.
8. Wait for the GitHub Actions confirmation comment.

## Required Issue Form Fields

- `team_id`
- `team_name`
- `student_names`
- `model_name`
- `num_parameters`
- `validation_accuracy`
- `validation_f1_macro`
- `predictions_csv_url`
- `ablations_md_url`

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

## Instructor Policy

Each `team_id` has only one visible latest submission. If a team submits again,
the files in `submissions/<team_id>/latest/` are overwritten.

All processed attempts that can be parsed are recorded in
`leaderboard/submissions_log.csv`. The public summary in
`leaderboard/latest_submissions.md` shows only the latest accepted submission per
team.

Hidden test evaluation is not implemented yet.


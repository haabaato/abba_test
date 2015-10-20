#!/usr/bin/python

import abba.stats
import argparse
import csv
import ipdb

def main():
  parser = argparse.ArgumentParser(
    description='Pass in a csv with 4 columns: # trials control, # trials variant, # successes control, # successes variant')
  parser.add_argument( "input", help="the input file")
  parser.add_argument(
    "-o", "--output", dest="output", default="abba_parse.csv",
    help="the output file")

  args = parser.parse_args()

  new_rows = []
  with open(args.input) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      new_rows.append(row)
      if not row[0][0].isdigit():
        row.extend(('Delta', 'P value'))
      else:
        num_trials_control = int(row[0])
        num_successes_control = int(row[2])
        num_trials_variant = int(row[1])
        num_successes_variant = int(row[3])

        experiment = abba.stats.Experiment(num_trials=2, baseline_num_successes=num_successes_control, baseline_num_trials=num_trials_control)
        results = experiment.get_results(num_successes=num_successes_variant, num_trials=num_trials_variant)
        delta = results.relative_improvement
        row.append('{:.2%} - {:.2%}'.format(delta.lower_bound, delta.upper_bound))
        row.append('{:2.3}'.format(results.two_tailed_p_value))
      print(', '.join(row))

  with open(args.output, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

if __name__ == "__main__":
    main()

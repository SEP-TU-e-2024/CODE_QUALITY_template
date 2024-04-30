import pandas as pd
import json

METRICS_FILE = "metrics.csv"
CONFIG_FILE = ".github/metrics_config.json"

# Colors
AQUA = '\033[94;1m'
TABLE_COL = ('\033[97;4m', '\033[37;4;2m')
END_COL = '\033[0m'

OPERATORS = {
    "=":  lambda a, b : a == b,
    "<=": lambda a, b : a <= b,
    "<":  lambda a, b : a < b,
    ">=": lambda a, b : a >= b,
    ">":  lambda a, b : a > b
}


def threshold(categories: list[pd.DataFrame], metric: str, threshold: list[str, int]) -> float:
    values = list()
    for category in categories:
        for ind in category.index:
            val = category[metric][ind]

            if type(val) == str:
                val = float(val.replace(',', '.'))
            
            values.append(val)

    if len(values) == 0:
        return 0.0
    print(metric, values)
    violations = 0
    op, t = threshold
    for val in values:
        if not OPERATORS[op](val, t):
            violations = violations + 1

    return violations / len(values)

def compute_percentages(categories: dict[str, pd.DataFrame], config: dict[str, dict]) -> dict[str, float]:
    percentages = dict()
    for key, val in config.items():
        dfs = [categories[t] for t in val['type'] if t in categories]
        percentages[key] = threshold(dfs, val['metric'], val['threshold'])
    
    return percentages

def percentage_to_rank(percentage: float) -> int:
    if percentage < 0.04:
        return 2
    if percentage < 0.06:
        return 1
    if percentage < 0.11:
        return 0
    if percentage < 0.21:
        return -1
    return -2

def compute_ranks(percentages: dict[str, float], config: dict[str, dict]) -> dict[str, float]:
    ranks = dict()

    for key, percentage in percentages.items():
        attrs = config[key]['attr']

        for attr in attrs:
            if attr not in ranks:
                ranks[attr] = list()
            
            ranks[attr].append(percentage_to_rank(percentage))

    for attr in ranks:
        ranks[attr] = sum(ranks[attr]) / len(ranks[attr])
    
    return ranks

def compute_grade(ranks: dict[str, float]) -> float:
    return (sum(ranks.values()) + 10) / 2

def nice_print(dictionary):
    MAXLEN = 30

    i = 0
    for key, val in dictionary.items():
        spaces = ' ' * max(0, MAXLEN - len(key))
        print(TABLE_COL[i % 2], key, spaces, val, END_COL)
        i += 1


def main():
    df = pd.read_csv(METRICS_FILE)

    categories = {c:df.loc[df.Kind == c].dropna(axis=1) for c in df.Kind.unique()}
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    percentages = compute_percentages(categories, config)
    ranks = compute_ranks(percentages, config)
    grade = compute_grade(ranks)

    print(f"{AQUA}Percentages{END_COL}")
    nice_print(percentages)
    print(f"{AQUA}Ranks{END_COL}")
    nice_print(ranks)
    print(f"{AQUA}Grade:{END_COL} ", grade)
    
if __name__ == "__main__":
    main()
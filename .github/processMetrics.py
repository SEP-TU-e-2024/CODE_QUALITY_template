import pandas as pd
import json

METRICS_FILE = "metrics.csv"
CONFIG_FILE = ".github/metrics_config.json"

OPERATORS = {
    "=":  lambda a, b : a == b,
    "<=": lambda a, b : a <= b,
    "<":  lambda a, b : a < b,
    ">=": lambda a, b : a >= b,
    ">":  lambda a, b : a > b
}


def threshold(category: pd.DataFrame, metric: str, threshold: list[str, int]) -> float:
    values = list()
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
        percentages[key] = threshold(categories[val['type']], val['metric'], val['threshold'])
    
    return percentages

def main():
    df = pd.read_csv(METRICS_FILE)

    categories = {c:df.loc[df.Kind == c].dropna(axis=1) for c in df.Kind.unique()}

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    print(categories)
    percentages = compute_percentages(categories, config)

    print(percentages)

    
    
if __name__ == "__main__":
    main()
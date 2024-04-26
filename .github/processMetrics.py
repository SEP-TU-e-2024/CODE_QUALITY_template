import pandas as pd

FILENAME = "metrics.csv"

def main():
    df = pd.read_csv(FILENAME)

    categories = {c:df.loc[df.Kind == c].dropna(axis=1) for c in df.Kind.unique()}

    for c in categories:
        print(categories[c])
    
    for c in categories:
        print(categories[c].columns.tolist())
        print()
    
    print(categories['Class'].CountDeclMethod)
    print(categories['Class'].CountClassBase)
    print(categories['Class'].CountClassCoupled)
    print(categories['Class'].CountClassCoupledModified)
    print(categories['Module File'].CountDeclFunction)
    print(categories['Module File'].CountLineCode)
    print(categories['Module File'].CountLineCodeDecl)
    print(categories['Module File'].CountLineCodeExe)
    print(categories['Module File'].CountStmt)
    print(categories['Module File'].CountStmtDecl)
    print(categories['Module File'].CountStmtExe)

if __name__ == "__main__":
    main()
# Python Midsem - My wrong answers

My marks scored: 72%
    (not sure how they calculated marks, i tried 2 ways and got ~50%, 63% - lower than they gave! obviously don't mention this)

Max possible marks (total 59):
- MCQ: 21 Qs (incl explanations), 1 point each => 21
- Code: Problem 1-5 (4 marks each), Problem 6-8 (6 marks each) => $5*4 + 3*6 = 38$
    - OR AS THEY HAVE GRADED 100 actually correct / 233 marked wrong / 800 total

Wrong answer marks deducted (1 marks actually correct / 14 marked wrong / 38 total):
- MCQ Q7,11 - 1x2 = 2 , x2 (accounting for explanations) - 4
- MCQ Q16 **WRONG MARKING!** - 1 (they put it wrong so 0 according to them)
- Code Problem 5 - 4 - *they gave 0%*
- Code Problem 7 - 6 *they gave 0%*
- Code Problem 8 - 6 marks, I passed 2/3 private tests, so *they gave 67 / 100*

## MCQ

**THEIR MCQ TOTAL SEEMS WRONG** - they gave 50 (didn't mention out of how much, assuming 100 as all rest problems seem out of 100)
   Don't understand how they calculated - acc their scoring I should have 16 / 21 = 76.19% (TODO: RECHECK TO CONFIRM)
   - this wrong calc seems because they have marked all correct explanations 0 due to not matching their exact wording

NOTE: they clarified that explanation is marked correct by them when answers are correct, even though on shared site it shows wrong.
TODO: calculate marks & make sure!

NOTE: (in general) Odd nums are actual questions, even nums are just where we had to put explanations for previous actual question. eg. (Q1 (question), Q2 (explanation for Q1))

-------------

*Numpy Broadcasting mistake (both (1,) and less shape dimensions)*:

Q7. If a and b are two dimensional NumPy arrays with shapes (2, 3, 4) and (1, 4). What will be shape of the output array when a*b is performed? If the operation results in an error, write the answer as "None", else write the shape in this form (x,y) or (x,y,z) without spaces in between.

My Answer: None

Correct Answer: (2,3,4) - explanation: NumPy treats (1,4) as (1,1,4), broadcasts it to match (2,3,4),the leading 1 expands to 2, the middle 1 expands to 3, so elementwise multiplication works and the resulting shape is (2,3,4)

---------------

*Numpy Slicing mistake (slicing gives view, NOT copy)*:

Q11. What is output of this code:

```python
a = np.array([[1,2,3], [4,5,6]])
b = a[:, :2]
b[0,0] = 99
print(a[0,0])
```

My answer: 2

Correct Answer: 99

-----------------

**INCORRECT MARKING IN Q16!** (score: 1 for answer only (no explanation asked for this))
   "object" is commonly used synonymously with "instance" in Python community - eg. in this blog post: https://medium.com/swlh/class-and-object-attributes-python-8191dcd1f4cf

Q16. What type of attributes are unique to each individual object created from a given class?

My Answer: Object attributes / Properties

Correct Answer: Instance attributes

## Code Questions

Problem 5: 2D Min-Max Normalization (Marks allotted - 4 Marks) - *they gave: 0 / 100*

Write a function two_d_norm(X) that normalizes a 2D matrix X so all elements lie between 0 and 1 using global min-max normalization.

Formula: X_norm = (X - X_min) / (X_max - X_min)

Example:

```python
import numpy as np

X = np.array([[1, 2], [3, 4]])
print(two_d_norm(X))
# Expected Output: [[0.   0.33]
#                   [0.67 1.  ]]
```

MY ANSWER: (didn't pass 1 public test even!) - because I stupidly used wrong formula!! (in denominator actual is max - min)

```python
def two_d_norm(X):
   X = X.astype(float)
   denom = np.where(X == np.max(X), 1, X - np.max(X))
   X_norm = (X - np.min(X)) / denom
   return X_norm
```

CORRECT ANSWER:

```python
def two_d_norm(X):
    X_min = X.min()
    X_max = X.max()
    X_norm = (X - X_min) / (X_max - X_min)
    return X_norm
```

-----------

**UPDATE FROM THEIR SIDE**: my code is wrong - I missed condition that regular 10% discount is *only if amount > 1000*.

Problem 7: Apply Discount (Marks allotted - 6 Marks) - *they gave: 0 / 100*

Write apply_discount(order_list) which applies discounts using a lambda function based on customer type:

    Prime: 20% discount (multiply by 0.8)
    Regular: 10% discount if amount > 1000 (multiply by 0.9), else no discount
    Guest: No discount

Input format: List of tuples [(customer_type, amount), ...]

MY ANSWER:

```python
def apply_discount(order_list):
    discounted_ratios = {
        'prime': 0.8,
        'regular': 0.9,
        'guest': 1
    }
    get_price = lambda name, price: float(discounted_ratios[name.lower()] * price)
    return [get_price(name, price) for name, price in order_list]
```

their 2 private tests shown failing, but actual and expected outputs match!!

Private test 1 (both actual & expected outputs same): `[400.0, 1200.0, 1800.0, 800.0, 3000.0]`

Private test 2 (both actual & expected outputs same): `[80000.0, 900.9, 99999.0, 999.0, 40.0]`

-----------

Problem 8: Group Sales Total (6 marks)

Write group_sales_total(data_dict, month_filter, group_var, group_value) that:

- Converts a dictionary to a Pandas DataFrame
- Filters rows by the specified month
- Groups by the group_var column
- Sums the "Sales" column
- Returns the total for the specified group_value (or 0 if not found)

MY ANSWER: 

```python
def group_sales_total(data_dict, month_filter, group_var, group_value):
    df = pd.DataFrame(data_dict)
    df = df[df["Month"] == month_filter]
    gdf = df.groupby(group_var).get_group(group_value)
    return gdf["Sales"].sum() if not gdf.empty else 0
```

PRIVATE CASE (2/3 pass, 1 fail, failing info below):

*Errored as didn't consider edge case where given `group_value` (here "Central") not in df*

TEST CODE & INPUT:

```python
sales_data = {
    "Region": ["North", "South", "East", "West", "North", "East", "South", "West"],
    "Product": ["A", "A", "B", "B", "C", "C", "A", "B"],
    "Sales": [1200, 800, 600, 900, 1500, 3829, 650, 6968],
    "Month": ["Jan", "Jan", "Feb", "Feb", "Jan", "Feb", "Feb", "Jan"],
}
is_equal(group_sales_total(sales_data, "Jan", "Region", "Central"), 0)
```

Expected Output: `0`

Actual Output (my program errored):

```python
Traceback (most recent call last):\n
  File "test.py", line 60, in <module>\n
    exec(sys.stdin.read())\n
  File "<string>", line 7, in <module>\n
  File "test.py", line 7, in group_sales_total\n
    gdf = df.groupby(group_var).get_group(group_value)\n
  File "/usr/local/lib/python3.6/dist-packages/pandas/core/groupby/groupby.py", line 810, in get_group\n
    raise KeyError(name)\n
KeyError: 'Central'
```



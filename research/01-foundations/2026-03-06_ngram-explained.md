# N-gram

DATE: 2026-03-06
> TYPE:  /
> :  n-gram ,

---

##  N-gram?

> :N-gram -N-().

> :.

---

##

### :"hello"

```text
1-gram (unigram) -- 单个字符:
  ["h", "e", "l", "l", "o"]

2-gram (bigram) -- 连续 2 个字符:
  ["he", "el", "ll", "lo"]

3-gram (trigram) -- 连续 3 个字符:
  ["hel", "ell", "llo"]

4-gram -- 连续 4 个字符:
  ["hell", "ello"]

5-gram -- 连续 5 个字符:
  ["hello"]
```

###

```text
文本:  h  e  l  l  o
        +--+  <- 2-gram: "he"
           +--+  <- 2-gram: "el"
              +--+  <- 2-gram: "ll"
                 +--+  <- 2-gram: "lo"

窗口大小 = 2,每次滑动 1 个字符
```

---

##  N-gram?

### :

```text
文本 1: "hello"
文本 2: "hallo"

完全匹配: 不匹配(完全不同)

但人类看出:很像!只有 1 个字母不同.
```

### N-gram :

```text
"hello" 的 2-grams: ["he", "el", "ll", "lo"]
"hallo" 的 2-grams: ["ha", "al", "ll", "lo"]

共同 2-grams: ["ll", "lo"] (2/4 = 50% 相似)

结论:部分匹配,相似度 50%
```

---

##

### 1.

```text
用户搜索:"hello"
文档:"hallo world"

传统匹配: 找不到("hello" != "hallo")

N-gram 匹配:
  搜索 2-grams: ["he", "el", "ll", "lo"]
  文档 2-grams: ["ha", "al", "ll", "lo", "o ", " w", ...]
  共同:["ll", "lo"]

  相似度:2/4 = 50%

  结果:找到相似内容!
```

### 2.

```text
用户输入:"helo" (拼写错误)

候选词:
  - "hello" (2-gram 重叠:["el", "ll", "lo"] = 3/4)
  - "help" (2-gram 重叠:["el", "ll"] = 2/4)
  - "hero" (2-gram 重叠:["el"] = 1/4)

推荐:"hello" (最相似)
```

### 3.

```text
英文特征 3-grams: "the", "ing", "and", "ion"
德文特征 3-grams: "sch", "ung", "cht", "ein"
法文特征 3-grams: "ion", "ent", "les", "ait"

文本:"This is interesting"
3-grams: ["Thi", "his", "is ", "s i", " in", "int", "nte", "ter", "ere", "res", "est", "sti", "tin", "ing"]

包含 "ing", "the" (部分) -> 可能是英文
```

### 4.

```text
文档 A: "The quick brown fox jumps"
文档 B: "The quick brown fox runs"

5-gram 重叠:
  A: ["The q", "he qu", "e qui", "quick", ..., "fox j", "ox ju", "x jum", " jump", "jumps"]
  B: ["The q", "he qu", "e qui", "quick", ..., "fox r", "ox ru", "x run", " run", "runs"]

共同 5-grams: 大部分相同(除了最后几个)

结论:高度相似,可能是重复/抄袭
```

---

##

### Jaccard

```text
两个文本的 n-gram 集合:
  A = ngrams(文本 1)
  B = ngrams(文本 2)

相似度 = |A INTERSECT B| / |A UNION B|
       = 共同 n-gram 数 / 总 n-gram 数

例:
  A = ["he", "el", "ll", "lo"]
  B = ["ha", "al", "ll", "lo"]

  A INTERSECT B = ["ll", "lo"] (2 个)
  A UNION B = ["he", "el", "ll", "lo", "ha", "al"] (6 个)

  相似度 = 2/6 = 0.33
```

###  N

```text
N=1 (unigram):
  优点:简单,快速
  缺点:丢失顺序信息("hello" 和 "olleh" 相同)

N=2 (bigram):
  优点:保留部分顺序,计算快
  缺点:上下文有限

N=3 (trigram):
  优点:更好的上下文
  缺点:更多 n-grams,占用空间

N=5+:
  优点:很好的上下文
  缺点:非常多 n-grams,稀疏

常用:N=2 到 N=5
```

---

##

### Python

```python
def get_ngrams(text, n=2):
    """
    获取文本的 n-grams.

    Args:
        text: 输入文本
        n: n-gram 大小

    Returns:
        n-gram 列表
    """
    ngrams = []
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        ngrams.append(ngram)
    return ngrams

#
text = "hello"
print(get_ngrams(text, 2))  # 2-grams
# :['he', 'el', 'll', 'lo']

print(get_ngrams(text, 3))  # 3-grams
# :['hel', 'ell', 'llo']
```text

### 构建索引

```
def build_ngram_index(documents, n=2):
    """
>      n-gram .

    Args:
>         documents:  [(doc_id, text), ...]
>         n: n-gram

    Returns:
>         :{ngram: [doc_ids]}
    """
    index = defaultdict(list)

    for doc_id, text in documents:
        ngrams = get_ngrams(text, n)
>         for ngram in set(ngrams):  # ,
            index[ngram].append(doc_id)

    return index

#
docs = [
    (1, "hello world"),
    (2, "hallo welt"),
    (3, "goodbye world")
]

index = build_ngram_index(docs, n=2)

# : "ll"?
> print(index["ll"])  # :[1, 2] ("hello"  "hallo"  "ll")
```text

---

## 在 traceflux 中的应用

### 当前设计(字符级 + n-gram)

```
> Level 0:
  "hello" -> [('h',0), ('e',1), ('l',2), ('l',3), ('o',4)]

> Level 1: N-gram
  "hello" -> 2-grams: ["he", "el", "ll", "lo"]
             3-grams: ["hel", "ell", "llo"]

> Level 2:
>   n-gram "he"  "ll"  ->
```text

### 查询处理

```
> :"hello"

> 1.  n-grams:
   ["he", "el", "ll", "lo"]

> 2. :
>     1: ["he", "el", "ll", "lo"] -> 4/4  (100%)
>     2: ["ha", "al", "ll", "lo"] -> 2/4  (50%)
>     3: ["go", "oo", "od"] -> 0/4  (0%)

> 3. ():
>    1.  1 (100%)
>    2.  2 (50%)
>    3.  3 (0%)
```text

---

## 优缺点总结

### 优点

| 优点 | 说明 |
|------|------|
| **简单** | 容易理解和实现 |
| **快速** | O(n) 时间复杂度 |
| **模糊匹配** | 支持部分匹配,不要求完全相同 |
| **语言无关** | 适用于任何语言(基于字符) |
| **无需词典** | 不需要预定义词汇表 |

### 缺点

| 缺点 | 说明 |
|------|------|
| **空间占用** | 大量 n-grams,索引较大 |
| **丢失长距离依赖** | 只捕捉局部模式(窗口内) |
| **参数选择** | 需要选择合适的 N 值 |
| **稀疏性** | 大 N 值导致很多 n-grams 只出现一次 |

---

## 与其他技术对比

| 技术 | 原理 | 适用场景 |
|------|------|----------|
| **N-gram** | 连续 N 个字符 | 模糊匹配,拼写检查 |
| **全文搜索** | 词级索引 | 精确词匹配 |
| **向量嵌入** | 语义向量 | 语义相似度 |
| **正则表达式** | 模式匹配 | 结构化搜索 |

N-GRAM-定位:简单,快速,模糊匹配的首选.

---

## 关键要点

1. **N-gram = 连续 N 个字符的序列**
2. **用于模糊匹配** -- 不要求完全相同
3. **N 越大,上下文越好,但空间越大**
4. **简单高效** -- O(n) 时间,易于实现
5. **语言无关** -- 适用于任何文本

---

状态: N-gram 技术说明完成
相关: `2026-03-06_character-level-analysis.md` (字符级分析)
下一步: 在 traceflux 中实现 n-gram 索引?

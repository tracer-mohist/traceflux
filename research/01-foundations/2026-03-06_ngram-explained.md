# N-gram 技术简介

**Date**: 2026-03-06  
**Type**: 技术说明 / 基础概念  
**目的**: 解释 n-gram 是什么，如何用

---

## 什么是 N-gram？

**定义**：N-gram 是**连续的 N 个字符（或词）的序列**。

**核心思想**：把文本切成固定长度的小片段。

---

## 直观示例

### 文本："hello"

```
1-gram (unigram) — 单个字符：
  ["h", "e", "l", "l", "o"]

2-gram (bigram) — 连续 2 个字符：
  ["he", "el", "ll", "lo"]

3-gram (trigram) — 连续 3 个字符：
  ["hel", "ell", "llo"]

4-gram — 连续 4 个字符：
  ["hell", "ello"]

5-gram — 连续 5 个字符：
  ["hello"]
```

### 滑动窗口视图

```
文本：  h  e  l  l  o
        └──┘  ← 2-gram: "he"
           └──┘  ← 2-gram: "el"
              └──┘  ← 2-gram: "ll"
                 └──┘  ← 2-gram: "lo"

窗口大小 = 2，每次滑动 1 个字符
```

---

## 为什么要用 N-gram？

### 问题：直接匹配整个文本太严格

```
文本 1: "hello"
文本 2: "hallo"

完全匹配：❌ 不匹配（完全不同）

但人类看出：很像！只有 1 个字母不同。
```

### N-gram 方案：局部匹配

```
"hello" 的 2-grams: ["he", "el", "ll", "lo"]
"hallo" 的 2-grams: ["ha", "al", "ll", "lo"]

共同 2-grams: ["ll", "lo"] (2/4 = 50% 相似)

结论：部分匹配，相似度 50%
```

---

## 应用场景

### 1. 模糊搜索

```
用户搜索："hello"
文档："hallo world"

传统匹配：❌ 找不到（"hello" ≠ "hallo"）

N-gram 匹配：
  搜索 2-grams: ["he", "el", "ll", "lo"]
  文档 2-grams: ["ha", "al", "ll", "lo", "o ", " w", ...]
  共同：["ll", "lo"]
  
  相似度：2/4 = 50%
  
  结果：找到相似内容！
```

### 2. 拼写检查

```
用户输入："helo" (拼写错误)

候选词：
  - "hello" (2-gram 重叠：["el", "ll", "lo"] = 3/4)
  - "help" (2-gram 重叠：["el", "ll"] = 2/4)
  - "hero" (2-gram 重叠：["el"] = 1/4)

推荐："hello" (最相似)
```

### 3. 语言识别

```
英文特征 3-grams: "the", "ing", "and", "ion"
德文特征 3-grams: "sch", "ung", "cht", "ein"
法文特征 3-grams: "ion", "ent", "les", "ait"

文本："This is interesting"
3-grams: ["Thi", "his", "is ", "s i", " in", "int", "nte", "ter", "ere", "res", "est", "sti", "tin", "ing"]

包含 "ing", "the" (部分) → 可能是英文
```

### 4. 文本去重

```
文档 A: "The quick brown fox jumps"
文档 B: "The quick brown fox runs"

5-gram 重叠：
  A: ["The q", "he qu", "e qui", "quick", ..., "fox j", "ox ju", "x jum", " jump", "jumps"]
  B: ["The q", "he qu", "e qui", "quick", ..., "fox r", "ox ru", "x run", " run", "runs"]

共同 5-grams: 大部分相同（除了最后几个）
  
结论：高度相似，可能是重复/抄袭
```

---

## 数学原理

### Jaccard 相似度

```
两个文本的 n-gram 集合：
  A = ngrams(文本 1)
  B = ngrams(文本 2)

相似度 = |A ∩ B| / |A ∪ B|
       = 共同 n-gram 数 / 总 n-gram 数

例：
  A = ["he", "el", "ll", "lo"]
  B = ["ha", "al", "ll", "lo"]
  
  A ∩ B = ["ll", "lo"] (2 个)
  A ∪ B = ["he", "el", "ll", "lo", "ha", "al"] (6 个)
  
  相似度 = 2/6 = 0.33
```

### 选择 N 的大小

```
N=1 (unigram):
  优点：简单，快速
  缺点：丢失顺序信息（"hello" 和 "olleh" 相同）
  
N=2 (bigram):
  优点：保留部分顺序，计算快
  缺点：上下文有限
  
N=3 (trigram):
  优点：更好的上下文
  缺点：更多 n-grams，占用空间
  
N=5+:
  优点：很好的上下文
  缺点：非常多 n-grams，稀疏

常用：N=2 到 N=5
```

---

## 实现示例

### Python 实现

```python
def get_ngrams(text, n=2):
    """
    获取文本的 n-grams。
    
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

# 示例
text = "hello"
print(get_ngrams(text, 2))  # 2-grams
# 输出：['he', 'el', 'll', 'lo']

print(get_ngrams(text, 3))  # 3-grams
# 输出：['hel', 'ell', 'llo']
```

### 构建索引

```python
def build_ngram_index(documents, n=2):
    """
    为文档集合构建 n-gram 倒排索引。
    
    Args:
        documents: 文档列表 [(doc_id, text), ...]
        n: n-gram 大小
    
    Returns:
        倒排索引：{ngram: [doc_ids]}
    """
    index = defaultdict(list)
    
    for doc_id, text in documents:
        ngrams = get_ngrams(text, n)
        for ngram in set(ngrams):  # 去重，避免同一文档重复计数
            index[ngram].append(doc_id)
    
    return index

# 示例
docs = [
    (1, "hello world"),
    (2, "hallo welt"),
    (3, "goodbye world")
]

index = build_ngram_index(docs, n=2)

# 查询：哪些文档包含 "ll"？
print(index["ll"])  # 输出：[1, 2] ("hello" 和 "hallo" 都有 "ll")
```

---

## 在 traceflux 中的应用

### 当前设计（字符级 + n-gram）

```
Level 0: 字符序列
  "hello" → [('h',0), ('e',1), ('l',2), ('l',3), ('o',4)]

Level 1: N-gram 抽象
  "hello" → 2-grams: ["he", "el", "ll", "lo"]
             3-grams: ["hel", "ell", "llo"]

Level 2: 共现分析
  n-gram "he" 和 "ll" 在同一片段出现 → 关联
```

### 查询处理

```
用户搜索："hello"

1. 提取查询 n-grams:
   ["he", "el", "ll", "lo"]

2. 查找匹配文档:
   文档 1: ["he", "el", "ll", "lo"] → 4/4 匹配 (100%)
   文档 2: ["ha", "al", "ll", "lo"] → 2/4 匹配 (50%)
   文档 3: ["go", "oo", "od"] → 0/4 匹配 (0%)

3. 返回结果（按相似度排序）:
   1. 文档 1 (100%)
   2. 文档 2 (50%)
   3. 文档 3 (0%)
```

---

## 优缺点总结

### 优点

| 优点 | 说明 |
|------|------|
| **简单** | 容易理解和实现 |
| **快速** | O(n) 时间复杂度 |
| **模糊匹配** | 支持部分匹配，不要求完全相同 |
| **语言无关** | 适用于任何语言（基于字符） |
| **无需词典** | 不需要预定义词汇表 |

### 缺点

| 缺点 | 说明 |
|------|------|
| **空间占用** | 大量 n-grams，索引较大 |
| **丢失长距离依赖** | 只捕捉局部模式（窗口内） |
| **参数选择** | 需要选择合适的 N 值 |
| **稀疏性** | 大 N 值导致很多 n-grams 只出现一次 |

---

## 与其他技术对比

| 技术 | 原理 | 适用场景 |
|------|------|----------|
| **N-gram** | 连续 N 个字符 | 模糊匹配、拼写检查 |
| **全文搜索** | 词级索引 | 精确词匹配 |
| **向量嵌入** | 语义向量 | 语义相似度 |
| **正则表达式** | 模式匹配 | 结构化搜索 |

**N-gram 定位**：简单、快速、模糊匹配的首选。

---

## 关键要点

1. **N-gram = 连续 N 个字符的序列**
2. **用于模糊匹配** — 不要求完全相同
3. **N 越大，上下文越好，但空间越大**
4. **简单高效** — O(n) 时间，易于实现
5. **语言无关** — 适用于任何文本

---

**状态**: N-gram 技术说明完成  
**相关**: `2026-03-06_character-level-analysis.md` (字符级分析)  
**下一步**: 在 traceflux 中实现 n-gram 索引？

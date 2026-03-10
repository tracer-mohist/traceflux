<!-- docs/PROMOTION-ISOLATION-DESIGN-v2.md -->
# traceflux 推广系统 - 完整隔离设计方案 v2

**日期**: 2026-03-07  
**状态**: 设计草案 v2 (响应用户反馈)  
**作者**: Tracer

---

## 核心洞察

### 推广的本质

**推广 = 曝光**，不是开发活动，而是**文档/记录活动**

| 维度 | 开发活动 | 推广活动 |
|------|---------|---------|
| **目的** | 构建功能 | 增加曝光 |
| **产出** | 代码 | PR、issue、文档 |
| **频率** | 持续 | 周期性 |
| **性质** | 创造性 | 事务性 |
| **存储** | 代码仓库 | 文档目录 |

### 关键设计原则

1. **星数筛选** - 选择有影响力的 awesome 列表 (高 stars = 高曝光)
2. **文档存储** - 推广是文档活动，存储在文档目录
3. **克隆仓库** - PR 行为需要克隆目标仓库 (间接状态)
4. **状态分层** - 克隆/PR/issue 都是间接状态说明

---

## 存储位置重新设计

### 方案对比

| 方案 | 位置 | 优点 | 缺点 |
|------|------|------|------|
| **A: 系统目录** | `~/.openclaw/promotions/` | OpenClaw 管理 | 与系统耦合，语义不清 |
| **B: 项目目录** | `traceflux/.github/` | 与项目绑定 | 污染项目，不适合多项目 |
| **C: 个人文档** | `~/tracer/docs/promotions/` ✅ | 语义清晰，个人活动 | 需要创建目录 |
| **D: 研究工作区** | `~/tracer/promotion-work/` | 独立工作区 | 与书房概念分离 |

### 推荐：方案 C + D 混合

```
~/tracer/                           # Tracer 个人书房
├── dev-repo/                       # 活跃开发项目
│   └── traceflux/                  # traceflux 源码
│
├── study-repo/                     # 研究学习项目
│   └── openclaw/                   # OpenClaw 源码 (只读)
│
├── promotion-work/                 # 推广工作区 (新增)
│   ├── traceflux/                  # 按项目分组
│   │   ├── docs/                   # 推广文档
│   │   │   ├── strategy.md         # 推广策略
│   │   │   ├── targets.md          # 目标列表 (带 stars 分析)
│   │   │   └── log.md              # 推广日志
│   │   ├── state/                  # 状态文件
│   │   │   ├── submissions.json    # 提交状态
│   │   │   └── rate-limit.json     # 速率限制
│   │   └── mirrors/                # 克隆的 awesome 仓库
│   │       ├── awesome-python/     # vinta/awesome-python fork
│   │       └── awesome-search/     # frutik/awesome-search fork
│
└── docs/                           # 个人文档 (可选)
    └── promotions/                 # 推广文档归档
        └── traceflux/
            └── history.md          # 推广历史 (冷数据)
```

### 为什么选择 `~/tracer/promotion-work/`

| 理由 | 说明 |
|------|------|
| **语义清晰** | "推广工作区"，一看就懂 |
| **个人活动** | 推广是 Tracer 的个人活动，不是 OpenClaw 系统活动 |
| **独立隔离** | 与项目代码、系统配置都分离 |
| **可扩展** | 未来推广其他项目，直接添加子目录 |
| **便于清理** | 推广结束后，整个目录可归档或删除 |

---

## 完整目录结构

```
~/tracer/promotion-work/
│
├── README.md                       # 推广系统说明
│
├── traceflux/                      # traceflux 推广专用
│   │
│   ├── docs/                       # 推广文档
│   │   ├── strategy.md             # 推广策略 (目标、原则)
│   │   ├── targets.md              # 目标 awesome 列表 (带 stars 分析)
│   │   ├── pr-templates/           # PR 模板
│   │   │   ├── awesome-python.md
│   │   │   └── awesome-search.md
│   │   └── log.md                  # 推广日志 (人类可读)
│   │
│   ├── state/                      # 状态文件 (机器可读)
│   │   ├── submissions.json        # 提交记录
│   │   ├── search-progress.json    # 搜索进度
│   │   ├── rate-limit.json         # 速率限制追踪
│   │   └── last-check-result.md    # 最近检查结果
│   │
│   ├── mirrors/                    # 克隆的 awesome 仓库 (间接状态)
│   │   ├── awesome-python/         # git clone + fork
│   │   │   ├── .git/
│   │   │   ├── README.md
│   │   │   └── ...
│   │   └── awesome-search/
│   │       └── ...
│   │
│   └── archive/                    # 归档 (冷数据)
│       ├── submissions-2026-03.json
│       └── weekly-summaries/
│           └── week-1.md
│
└── templates/                      # 通用模板 (可复用)
    ├── target-analysis.md          # 目标分析模板
    ├── pr-template.md              # PR 模板
    └── weekly-summary.md           # 周报模板
```

---

## 状态分层设计

### 三层状态模型

```
┌─────────────────────────────────────────────────────────┐
│  热状态 (Hot State) - 频繁变化                          │
│  位置：~/tracer/promotion-work/traceflux/state/         │
│  内容：PR 状态、检查记录、速率限制                       │
│  格式：JSON (机器可读)                                   │
│  备份：可选 (可从 GitHub 重建)                           │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 每日汇总
                          ▼
┌─────────────────────────────────────────────────────────┐
│  温状态 (Warm State) - 中等变化                         │
│  位置：~/tracer/promotion-work/traceflux/docs/          │
│  内容：推广日志、PR 草稿、目标分析                       │
│  格式：Markdown (人类可读)                               │
│  备份：Git 版本控制 (推广工作区独立仓库)                 │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 每周/每月归档
                          ▼
┌─────────────────────────────────────────────────────────┐
│  冷状态 (Cold State) - 很少变化                         │
│  位置：~/tracer/promotion-work/traceflux/archive/       │
│         或 ~/tracer/docs/promotions/traceflux/          │
│  内容：历史总结、里程碑记录                              │
│  格式：Markdown (人类可读)                               │
│  备份：Git 版本控制 (可选归档到项目仓库)                 │
└─────────────────────────────────────────────────────────┘
```

---

## 间接状态说明

### 什么是间接状态？

**直接状态**: `submissions.json` 中的记录
```json
{
  "repo": "vinta/awesome-python",
  "status": "pending",
  "prNumber": 12345
}
```

**间接状态**: 通过外部行为推断的状态
| 间接状态 | 说明 | 如何推断 |
|---------|------|---------|
| **克隆仓库存在** | 准备提交或已提交 | `ls ~/tracer/promotion-work/traceflux/mirrors/awesome-python/` |
| **克隆仓库有修改** | PR 已提交，等待合并 | `git status` 查看是否有未推送的修改 |
| **克隆仓库已删除** | PR 被拒或已合并 | 仓库完成使命，可清理 |
| **Fork 存在** | 已准备提交 | `gh repo view tracer-mohist/awesome-python` |
| **PR 存在** | 已提交 | `gh pr view vinta/awesome-python#12345` |

### 为什么需要间接状态？

1. **冗余验证** - 状态文件可能丢失，但克隆仓库是物理存在
2. **上下文保留** - 克隆仓库保留了提交时的完整上下文
3. **便于恢复** - 如需修改 PR，直接操作克隆仓库即可
4. **审计追踪** - Git 历史记录是天然的审计日志

### 克隆仓库生命周期

```
1. 搜索目标
   └─► 发现 vinta/awesome-python (stars: 180k)

2. 准备提交
   └─► Fork: gh repo fork vinta/awesome-python
   └─► 克隆：git clone <fork-url> mirrors/awesome-python

3. 提交 PR
   └─► 修改 README.md
   └─► 推送：git push
   └─► 创建 PR: gh pr create

4. 等待审核
   └─► 克隆仓库保留 (不删除)
   └─► 定期：git fetch upstream 检查状态

5. 结果处理
   ├─► 接受：保留克隆仓库 30 天，然后删除
   ├─► 拒绝：根据反馈修改，重新提交
   └─► 超时 (2 周无响应)：关闭 PR，删除克隆仓库
```

---

## 目标筛选策略

### 星数筛选标准

| 优先级 | 最少 Stars | 说明 | 预期曝光 |
|-------|-----------|------|---------|
| **Priority 1** | 10,000+ | 顶级列表，高曝光 | 极高 |
| **Priority 2** | 1,000+ | 知名列表，中等曝光 | 高 |
| **Priority 3** | 100+ | 垂直领域，精准曝光 | 中 |
| **Priority 4** | 50+ | 新兴列表，低曝光 | 低 |
| **跳过** | <50 | 影响力有限 | 极低 |

### 目标分析维度

```markdown
## vinta/awesome-python

**URL**: https://github.com/vinta/awesome-python  
**Stars**: 180,000+  
**Category**: Text Processing  
**Priority**: 1 (顶级)

**入选标准**:
- ✅ Stars > 10k (180k ✅)
- ✅ 活跃维护 (最近 commit < 1 个月)
- ✅ 有 CONTRIBUTING.md
- ✅ 接受新提交 (查看近期 merged PRs)

**提交要求**:
- 项目 stars: 50+ (traceflux 当前：XX)
- 项目年龄：30+ 天
- License: MIT/Apache

**预期曝光**: 极高 (Python 开发者必看)  
**竞争程度**: 高 (维护者严格)  
**建议**: 精心准备 PR 描述，突出独特价值
```

### 目标列表模板

**位置**: `~/tracer/promotion-work/traceflux/docs/targets.md`

```markdown
# traceflux 推广目标列表

**更新时间**: 2026-03-07  
**筛选标准**: Stars >= 100, 活跃维护

---

## Priority 1 (Stars 10k+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| vinta/awesome-python | 180k | Text Processing | 准备中 | - |
| sorrycc/awesome-javascript | 30k | JavaScript | 待提交 | - |

## Priority 2 (Stars 1k+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| frutik/awesome-search | 5k | Search | 已提交 | 2026-03-07 |
| akullpp/awesome-cpp | 20k | C++ | 待评估 | - |

## Priority 3 (Stars 100+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| ... | ... | ... | ... | ... |

---

## 已拒绝/跳过

| 仓库 | Stars | 原因 | 日期 |
|------|-------|------|------|
| some-repo/awesome-list | 30 | Stars < 100 | 2026-03-07 |
```

---

## 工作流程 v2

### 阶段 1: 目标搜索与分析

```
1. 搜索 awesome 列表
   执行：gh search repos "awesome-python" --limit 50
   输出：仓库列表 (含 stars、更新时间)

2. 筛选目标
   标准：stars >= 100, 最近 commit < 6 个月
   输出：候选列表

3. 分析目标
   检查：CONTRIBUTING.md、近期 PRs、接受率
   输出：目标分析文档 (docs/targets.md)

4. 确定优先级
   排序：stars 降序 + 相关性
   输出：提交顺序
```

### 阶段 2: 准备提交

```
1. 克隆仓库 (创建间接状态)
   执行：gh repo fork <target> --clone
   位置：~/tracer/promotion-work/traceflux/mirrors/<name>/

2. 准备 PR
   修改：README.md (添加 traceflux 条目)
   草稿：docs/pr-templates/<name>.md

3. 检查要求
   验证：项目 stars、年龄、license
   记录：state/submissions.json

4. 用户确认
   展示：PR 草稿、目标分析
   决策：提交/修改/放弃
```

### 阶段 3: 执行提交

```
1. 提交 PR
   执行：git push + gh pr create
   记录：更新 state/submissions.json

2. 保留克隆仓库
   状态：等待审核中
   操作：定期 git fetch upstream

3. 记录日志
   写入：docs/log.md
   格式：时间 | 操作 | 目标 | 结果
```

### 阶段 4: 跟踪与维护

```
1. 定期检查 (每 3 天)
   执行：gh pr view <repo>#<number>
   更新：state/submissions.json

2. 处理反馈
   情况：维护者提出修改意见
   操作：修改克隆仓库，push 更新

3. 结果处理
   接受：保留克隆 30 天，归档状态
   拒绝：分析原因，决定是否重试
   超时：关闭 PR，清理克隆仓库
```

---

## 状态文件设计 v2

### submissions.json

**位置**: `~/tracer/promotion-work/traceflux/state/submissions.json`

```json
{
  "meta": {
    "version": 2,
    "project": "traceflux",
    "createdAt": "2026-03-07T20:30:00+08:00",
    "lastUpdated": "2026-03-07T20:30:00+08:00"
  },
  
  "targets": {
    "vinta/awesome-python": {
      "priority": 1,
      "stars": 180000,
      "category": "Text Processing",
      "status": "preparing",
      "mirrorPath": "~/tracer/promotion-work/traceflux/mirrors/awesome-python",
      "prNumber": null,
      "prUrl": null,
      "submittedAt": null,
      "notes": "顶级列表，精心准备"
    },
    "frutik/awesome-search": {
      "priority": 2,
      "stars": 5000,
      "category": "Search Tools",
      "status": "pending",
      "mirrorPath": "~/tracer/promotion-work/traceflux/mirrors/awesome-search",
      "prNumber": 12345,
      "prUrl": "https://github.com/frutik/awesome-search/pull/12345",
      "submittedAt": "2026-03-07T20:30:00+08:00",
      "notes": "直接分类匹配"
    }
  },
  
  "history": [
    {
      "timestamp": "2026-03-07T20:30:00+08:00",
      "action": "fork-repo",
      "target": "frutik/awesome-search",
      "result": "success",
      "details": {
        "mirrorPath": "~/tracer/promotion-work/traceflux/mirrors/awesome-search"
      }
    },
    {
      "timestamp": "2026-03-07T20:35:00+08:00",
      "action": "create-pr",
      "target": "frutik/awesome-search",
      "result": "success",
      "details": {
        "prNumber": 12345,
        "prUrl": "https://github.com/frutik/awesome-search/pull/12345"
      }
    }
  ],
  
  "stats": {
    "totalSearched": 20,
    "totalSubmitted": 1,
    "accepted": 0,
    "rejected": 0,
    "pending": 1,
    "preparing": 1
  },
  
  "rateLimit": {
    "maxPerWeek": 2,
    "submissionsThisWeek": 1,
    "weekStartsAt": "2026-03-03T00:00:00+08:00",
    "lastSubmissionAt": "2026-03-07T20:30:00+08:00",
    "nextAllowedAt": "2026-03-14T20:30:00+08:00"
  }
}
```

### 推广日志 (人类可读)

**位置**: `~/tracer/promotion-work/traceflux/docs/log.md`

```markdown
# traceflux 推广日志

## 2026-03-07

### 10:30 - 搜索目标列表
- 搜索关键词："awesome-python", "awesome-search"
- 找到候选：20 个
- 筛选后：5 个 (stars >= 100)

### 11:00 - 分析目标
- vinta/awesome-python: 180k stars, Priority 1
- frutik/awesome-search: 5k stars, Priority 2

### 14:00 - 准备提交 (frutik/awesome-search)
- Fork 仓库：成功
- 克隆到：~/tracer/promotion-work/traceflux/mirrors/awesome-search
- 修改 README.md: 添加 traceflux 条目
- PR 草稿：docs/pr-templates/awesome-search.md

### 15:00 - 提交 PR
- PR #12345 创建成功
- URL: https://github.com/frutik/awesome-search/pull/12345
- 状态：pending

### 20:00 - 检查状态
- PR #12345: 无变化 (pending)
- 下次检查：2026-03-10

---

## 2026-03-10

### 10:00 - 检查状态
- PR #12345: 维护者评论，要求修改描述
- 操作：更新 PR 描述，push 修改

...
```

---

## 克隆仓库管理

### 目录结构

```
~/tracer/promotion-work/traceflux/mirrors/
├── awesome-python/               # vinta/awesome-python fork
│   ├── .git/
│   │   ├── config                # remote: upstream, origin
│   │   └── ...
│   ├── README.md                 # 已修改 (添加 traceflux)
│   └── ...
│
├── awesome-search/               # frutik/awesome-search fork
│   ├── .git/
│   │   ├── config
│   │   └── ...
│   ├── README.md
│   └── ...
│
└── README.md                     # 克隆仓库说明
```

### Git 远程配置

```bash
# 克隆后配置
cd ~/tracer/promotion-work/traceflux/mirrors/awesome-search/

# origin: 你的 fork
git remote -v
# origin  git@github.com:tracer-mohist/awesome-search.git (fetch)
# origin  git@github.com:tracer-mohist/awesome-search.git (push)

# upstream: 原始仓库
git remote add upstream git@github.com:frutik/awesome-search.git

# 定期同步
git fetch upstream
git status  # 查看是否有新 commit
```

### 清理策略

| 情况 | 操作 | 时间 |
|------|------|------|
| PR 接受 | 保留 30 天，然后删除 | 合并后 30 天 |
| PR 拒绝 (不重试) | 立即删除 | 决定不重试后 |
| PR 拒绝 (重试) | 保留，修改后重新提交 | 修改期间 |
| PR 超时 (无响应) | 删除 | 2 周无响应后 |

---

## 备份策略

### 推广工作区 Git 仓库

```bash
# 初始化推广工作区为 Git 仓库
cd ~/tracer/promotion-work/
git init
git add traceflux/
git commit -m "Initial promotion state for traceflux"

# 推送到私有仓库 (可选)
git remote add origin git@github.com:tracer-mohist/traceflux-promotion.git
git push -u origin main
```

### 归档到项目仓库 (冷数据)

```bash
# 每周归档
cd ~/tracer/promotion-work/traceflux/
cp state/submissions.json \
   ~/tracer/dev-repo/traceflux/.github/archive/promotion-state-20260307.json

cd ~/tracer/dev-repo/traceflux/
git add .github/archive/
git commit -m "Archive promotion state 2026-03-07"
```

---

## 目录创建脚本 v2

```bash
#!/bin/bash
# create-promotion-workspace.sh
# 创建推广工作区目录结构

PROJECT="traceflux"
BASE_DIR="/home/openclaw/tracer/promotion-work/$PROJECT"

# 创建目录结构
mkdir -p "$BASE_DIR/docs/pr-templates"
mkdir -p "$BASE_DIR/state"
mkdir -p "$BASE_DIR/mirrors"
mkdir -p "$BASE_DIR/archive/weekly-summaries"

# 创建 README
cat > "$BASE_DIR/README.md" << 'EOF'
# traceflux 推广工作区

**创建日期**: 2026-03-07

## 目录结构

- `docs/` - 推广文档 (策略、目标、日志)
- `state/` - 状态文件 (JSON, 机器可读)
- `mirrors/` - 克隆的 awesome 仓库 (间接状态)
- `archive/` - 归档 (冷数据)

## 快速开始

1. 查看目标列表：`cat docs/targets.md`
2. 查看当前状态：`cat state/submissions.json`
3. 查看推广日志：`cat docs/log.md`

## 克隆仓库

`mirrors/` 目录包含 fork + clone 的 awesome 列表仓库。
每个克隆仓库配置了：
- `origin`: 你的 fork
- `upstream`: 原始仓库

## 清理

推广结束后，整个目录可归档或删除。
EOF

# 创建初始状态文件
cat > "$BASE_DIR/state/submissions.json" << EOF
{
  "meta": {
    "version": 2,
    "project": "$PROJECT",
    "createdAt": "$(date -Iseconds)",
    "lastUpdated": "$(date -Iseconds)"
  },
  "targets": {},
  "history": [],
  "stats": {
    "totalSearched": 0,
    "totalSubmitted": 0,
    "accepted": 0,
    "rejected": 0,
    "pending": 0,
    "preparing": 0
  },
  "rateLimit": {
    "maxPerWeek": 2,
    "submissionsThisWeek": 0,
    "weekStartsAt": "$(date -Iseconds)",
    "lastSubmissionAt": null
  }
}
EOF

# 创建目标分析模板
cat > "$BASE_DIR/docs/targets.md" << 'EOF'
# traceflux 推广目标列表

**更新时间**: YYYY-MM-DD  
**筛选标准**: Stars >= 100, 活跃维护

---

## Priority 1 (Stars 10k+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| | | | 待分析 | - |

## Priority 2 (Stars 1k+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| | | | 待分析 | - |

## Priority 3 (Stars 100+)

| 仓库 | Stars | Category | 状态 | 提交日期 |
|------|-------|----------|------|---------|
| | | | 待分析 | - |
EOF

# 创建推广日志
cat > "$BASE_DIR/docs/log.md" << 'EOF'
# traceflux 推广日志

## YYYY-MM-DD

### HH:MM - 操作描述
- 详情 1
- 详情 2

---
EOF

echo "Created promotion workspace for $PROJECT at $BASE_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $BASE_DIR"
echo "  2. Edit docs/targets.md (add target awesome lists)"
echo "  3. Search awesome lists: gh search repos \"awesome-python\" --limit 50"
echo "  4. Analyze targets and update docs/targets.md"
```

---

## 决策记录

### 决策 1: 使用 `~/tracer/promotion-work/` 作为存储位置

**日期**: 2026-03-07  
**决策**: 推广工作区放在个人书房目录

**理由**:
1. 推广是 Tracer 的个人活动，不是 OpenClaw 系统活动
2. `~/tracer/` 是"书房"概念，符合文档/研究性质
3. 独立于项目代码 (`dev-repo/`) 和研究 (`study-repo/`)
4. 语义清晰：`promotion-work` = 推广工作区

---

### 决策 2: 克隆仓库作为间接状态

**日期**: 2026-03-07  
**决策**: 克隆目标 awesome 仓库到 `mirrors/` 目录

**理由**:
1. PR 行为需要本地仓库
2. 克隆仓库是物理存在的状态证明
3. 便于修改和重新提交
4. Git 历史是天然审计日志

---

### 决策 3: 星数筛选标准

**日期**: 2026-03-07  
**决策**: 优先选择高 stars 列表 (曝光最大化)

**标准**:
- Priority 1: 10k+ stars (顶级曝光)
- Priority 2: 1k+ stars (知名列表)
- Priority 3: 100+ stars (垂直领域)
- 跳过：<100 stars (影响力有限)

**理由**:
- 推广本质是曝光
- 高 stars = 高流量 = 高曝光
- 时间有限，优先高价值目标

---

## 下一步行动

### 立即执行

- [ ] 运行创建脚本：`bash create-promotion-workspace.sh`
- [ ] 搜索 awesome 列表：`gh search repos "awesome-python" --limit 50`
- [ ] 分析目标：填写 `docs/targets.md`
- [ ] 选择第一个目标：frutik/awesome-search (直接匹配)

### 第一次提交

- [ ] Fork 仓库：`gh repo fork frutik/awesome-search --clone`
- [ ] 移动到 mirrors: `mv awesome-search ~/tracer/promotion-work/traceflux/mirrors/`
- [ ] 配置 upstream: `git remote add upstream ...`
- [ ] 修改 README.md
- [ ] 用户确认 PR 草稿
- [ ] 提交 PR

### 后续优化

- [ ] 根据经验调整目录结构
- [ ] 建立归档流程
- [ ] 初始化推广工作区 Git 仓库 (可选)
- [ ] 总结经验文档

---

## 相关文件

- `docs/PROMOTION-ISOLATION-DESIGN.md` - v1 设计 (废弃)
- `docs/PROMOTION-STRATEGY-DESIGN.md` - 策略设计
- `docs/AWESOME-PROMOTION-DESIGN.md` - 技术设计

---

**设计原则**: 语义清晰、隔离完整、便于管理  
**核心理念**: 推广是文档活动，不是开发活动

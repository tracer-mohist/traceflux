<!-- docs/PROMOTION-ISOLATION-DESIGN.md -->
# traceflux 推广系统 - 完整隔离设计方案

**日期**: 2026-03-07  
**状态**: 设计草案 v2  
**作者**: Tracer

---

## 核心问题

### 需要隔离什么？

| 需要隔离的内容 | 原因 |
|---------------|------|
| **会话历史** | 推广任务频繁、琐碎，污染主会话记忆 |
| **状态文件** | 推广专用数据，不应混入项目代码 |
| **日志记录** | 大量检查日志，与主任务无关 |
| **配置信息** | 推广专用配置 (速率限制、目标列表等) |
| **临时文件** | PR 草稿、提交模板等一次性文件 |

### 隔离层级

```
┌─────────────────────────────────────────────────────────┐
│                    主会话 (Main Session)                 │
│  - 用户直接交互                                          │
│  - 核心记忆 (MEMORY.md)                                  │
│  - 项目决策                                              │
│  - ⚠️ 避免：推广任务细节、检查日志                       │
└─────────────────────────────────────────────────────────┘
                          │
                          │ sessions_spawn (隔离边界)
                          ▼
┌─────────────────────────────────────────────────────────┐
│              推广会话 (Promotion Session)                │
│  - 独立会话 ID                                           │
│  - 独立会话日志                                          │
│  - 专用工具上下文                                        │
│  - ✅ 执行：检查、搜索、提交                             │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 文件系统 (隔离存储)
                          ▼
┌─────────────────────────────────────────────────────────┐
│              推广存储目录 (Promotion Storage)            │
│  - 状态文件                                              │
│  - 日志文件                                              │
│  - 配置文件                                              │
│  - 临时文件                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 方案一：项目内存储 (当前方案)

### 目录结构

```
/home/openclaw/tracer/dev-repo/traceflux/
├── .github/
│   ├── awesome-submissions.json    # 状态跟踪
│   └── awesome-check-result.md     # 检查结果
├── docs/
│   ├── PROMOTION-STRATEGY-DESIGN.md  # 策略设计
│   └── AWESOME-PROMOTION-DESIGN.md   # 技术设计
└── scripts/
    └── check-awesome-status.py     # 检查脚本
```

### 优点

- ✅ 与项目代码在一起
- ✅ Git 版本控制 (自动)
- ✅ 结构简单

### 缺点

- ❌ 与项目代码混杂
- ❌ 推广日志污染项目仓库
- ❌ 如果推广多个项目，每个项目都要重复配置
- ❌ 状态文件与代码耦合

### 适用场景

- 单一项目推广
- 推广频率低 (日志少)
- 希望状态与项目绑定

---

## 方案二：独立存储目录 (推荐)

### 目录结构

```
/home/openclaw/.openclaw/promotions/          # OpenClaw 推广专用目录
├── traceflux/                                # 按项目分组
│   ├── state/
│   │   ├── submissions.json                  # 提交状态
│   │   ├── search-progress.json              # 搜索进度
│   │   └── rate-limit.json                   # 速率限制追踪
│   ├── logs/
│   │   ├── 2026-03-07-check.log              # 检查日志
│   │   ├── 2026-03-07-submit.log             # 提交日志
│   │   └── 2026-03-08-check.log
│   ├── drafts/
│   │   ├── awesome-python-pr.md              # PR 草稿
│   │   └── awesome-search-pr.md
│   └── config/
│       ├── targets.json                      # 目标列表配置
│       └── constraints.json                  # 约束条件
│
├── llm-api-scope/                            # 未来其他项目
│   ├── state/
│   ├── logs/
│   └── ...
│
└── README.md                                 # 推广系统说明
```

### 优点

- ✅ 完全隔离 (与项目代码分离)
- ✅ 集中管理 (多个项目推广统一位置)
- ✅ 日志独立 (不污染任何项目仓库)
- ✅ 配置可复用 (不同项目共享配置模板)
- ✅ 易于清理 (删除推广目录不影响项目)

### 缺点

- ❌ 需要额外目录
- ❌ 状态文件不在项目 Git 中 (需单独备份)
- ❌ 需要额外设计备份策略

### 适用场景

- 多项目推广
- 推广频率高 (日志多)
- 希望推广与项目解耦

---

## 方案三：混合方案 (最佳实践)

### 设计原则

**热数据** (频繁访问、当前活跃) → 独立存储目录  
**冷数据** (历史记录、最终状态) → 项目仓库

### 目录结构

```
# 热数据 (独立存储)
/home/openclaw/.openclaw/promotions/traceflux/
├── current-state.json              # 当前状态 (频繁读写)
├── active-drafts/                  # 活跃草稿
├── logs/                           # 运行日志
└── temp/                           # 临时文件

# 冷数据 (项目仓库)
/home/openclaw/tracer/dev-repo/traceflux/.github/
├── awesome-milestones.json         # 里程碑记录 (定期归档)
└── docs/PROMOTION-HISTORY.md       # 推广历史 (定期归档)
```

### 数据流

```
推广执行中:
  读写 → .openclaw/promotions/traceflux/current-state.json
  
每周归档:
  复制 → .github/awesome-milestones.json
  提交 → Git commit
  
每月总结:
  整理 → docs/PROMOTION-HISTORY.md
  提交 → Git commit
```

### 优点

- ✅ 热数据快速访问 (独立目录)
- ✅ 冷数据永久保存 (项目 Git)
- ✅ 日志不污染项目 (独立日志目录)
- ✅ 可追溯历史 (归档到项目)

---

## 推荐方案：方案二 (独立存储目录)

### 理由

1. **推广是跨项目的活动** - 未来可能推广多个项目
2. **日志量大** - 每次检查都产生日志，不应污染项目
3. **配置可复用** - 不同项目的推广策略相似
4. **易于管理** - 集中查看所有推广活动

### Git 备份策略

虽然状态文件不在项目 Git 中，但可以:

```bash
# 方案 A: 推广目录独立 Git 仓库
cd /home/openclaw/.openclaw/promotions/
git init
git add traceflux/
git commit -m "Initial promotion state"
# 推送到私有仓库 (可选)

# 方案 B: 定期归档到项目
cd /home/openclaw/tracer/dev-repo/traceflux/
cp ~/.openclaw/promotions/traceflux/state/submissions.json .github/
git add .github/submissions.json
git commit -m "Archive promotion state 2026-03-07"

# 方案 C: 不备份 (可接受损失)
# 推广状态丢失可重建，不是关键数据
```

---

## 完整工作流程设计

### 阶段 1: 手动触发 (当前)

```
┌─────────────────────────────────────────────────────────┐
│  1. 用户发起 (主会话)                                    │
│     "检查 traceflux awesome list 状态"                   │
└─────────────────────────────────────────────────────────┘
                          │
                          │ sessions_spawn
                          ▼
┌─────────────────────────────────────────────────────────┐
│  2. 独立会话执行                                         │
│     会话标签：traceflux-awesome-check-20260307          │
│     会话模式：run (一次性)                               │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 执行步骤
                          ▼
┌─────────────────────────────────────────────────────────┐
│  3. 加载配置                                             │
│     读取：~/.openclaw/promotions/traceflux/config/      │
│       - targets.json (目标列表)                          │
│       - constraints.json (约束条件)                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  4. 检查状态                                             │
│     读取：~/.openclaw/promotions/traceflux/state/       │
│       - submissions.json (提交记录)                      │
│     执行：gh pr view <repo>#<number>                    │
│     更新：submissions.json                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  5. 记录日志                                             │
│     写入：~/.openclaw/promotions/traceflux/logs/        │
│       - 2026-03-07-check.log                            │
│     格式：时间戳 | 操作 | 结果 | 详情                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  6. 生成报告                                             │
│     写入：~/.openclaw/promotions/traceflux/state/       │
│       - last-check-result.md                            │
│     内容：状态变化、建议操作                             │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 返回结果
                          ▼
┌─────────────────────────────────────────────────────────┐
│  7. 用户查看 (主会话)                                    │
│     读取报告，决定下一步                                 │
│     如需提交：发起新的 sessions_spawn                   │
└─────────────────────────────────────────────────────────┘
```

---

## 状态存储设计

### 核心状态文件

**位置**: `~/.openclaw/promotions/traceflux/state/submissions.json`

```json
{
  "meta": {
    "version": 1,
    "project": "traceflux",
    "createdAt": "2026-03-07T20:30:00+08:00",
    "lastUpdated": "2026-03-07T20:30:00+08:00",
    "lastCheckAt": "2026-03-07T20:30:00+08:00"
  },
  
  "targets": {
    "vinta/awesome-python": {
      "status": "pending",
      "category": "Text Processing",
      "submittedAt": "2026-03-07T20:30:00+08:00",
      "prNumber": 12345,
      "prUrl": "https://github.com/vinta/awesome-python/pull/12345"
    }
  },
  
  "history": [
    {
      "timestamp": "2026-03-07T20:30:00+08:00",
      "action": "submit",
      "target": "vinta/awesome-python",
      "result": "success",
      "details": {
        "prNumber": 12345,
        "prUrl": "https://github.com/vinta/awesome-python/pull/12345"
      }
    },
    {
      "timestamp": "2026-03-07T20:35:00+08:00",
      "action": "check",
      "target": "vinta/awesome-python",
      "result": "no-change",
      "details": {
        "status": "pending"
      }
    }
  ],
  
  "stats": {
    "totalSubmitted": 1,
    "accepted": 0,
    "rejected": 0,
    "pending": 1,
    "withdrawn": 0
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

### 日志文件

**位置**: `~/.openclaw/promotions/traceflux/logs/YYYY-MM-DD-<type>.log`

**格式**:
```
2026-03-07T20:30:00+08:00 | check | start | session=traceflux-awesome-check-20260307
2026-03-07T20:30:01+08:00 | check | load-state | path=~/.openclaw/promotions/traceflux/state/submissions.json
2026-03-07T20:30:02+08:00 | check | gh-pr-view | repo=vinta/awesome-python pr=12345 status=pending
2026-03-07T20:30:03+08:00 | check | update-state | target=vinta/awesome-python old=pending new=pending
2026-03-07T20:30:04+08:00 | check | write-log | path=logs/2026-03-07-check.log
2026-03-07T20:30:05+08:00 | check | complete | changes=0 duration=5s
```

### 配置文件

**位置**: `~/.openclaw/promotions/traceflux/config/targets.json`

```json
{
  "priority1": [
    {
      "repo": "vinta/awesome-python",
      "category": "Text Processing",
      "reason": "Most popular Python list",
      "requirements": {
        "minStars": 50,
        "minAge": 30,
        "hasLicense": true
      }
    },
    {
      "repo": "frutik/awesome-search",
      "category": "Search Tools",
      "reason": "Direct category match",
      "requirements": {
        "minStars": 20,
        "minAge": 14
      }
    }
  ],
  
  "priority2": [
    {
      "repo": "awesomelistsio/awesome-nlp",
      "category": "NLP Tools",
      "reason": "Text analysis category"
    }
  ],
  
  "blacklist": []
}
```

---

## 执行周期设计

### 检查周期

| 任务类型 | 频率 | 触发方式 | 说明 |
|---------|------|---------|------|
| **状态检查** | 每 3 天 | 手动或 Cron | 检查 pending PR 状态 |
| **搜索新列表** | 每周 1 次 | 手动 | 寻找新的目标 awesome lists |
| **准备提交** | 按需 | 手动 | 准备 PR 草稿和材料 |
| **执行提交** | 按需 (最多 2/周) | 手动确认 | 提交 PR |
| **归档状态** | 每周 1 次 | 手动或自动 | 复制状态到项目仓库 |

### 周期可视化

```
Week 1 (2026-03-03 to 2026-03-09)
├─ Mon 03: 提交 #1 (frutik/awesome-search) ✅
├─ Wed 05: 检查状态 (无变化)
├─ Fri 07: 搜索新列表 (找到 3 个候选)
├─ Sat 08: 检查状态 (无变化)
└─ Sun 09: 归档状态到项目仓库

Week 2 (2026-03-10 to 2026-03-16)
├─ Mon 10: 检查状态 (#1 仍 pending)
├─ Wed 12: 检查状态 (#1 accepted! ✅)
├─ Thu 13: 提交 #2 (vinta/awesome-python) ✅
├─ Sat 15: 检查状态 (#2 pending)
└─ Sun 16: 归档状态到项目仓库
```

---

## 会话隔离设计

### 会话标签规范

**格式**: `promo-<project>-<task>-<date>`

| 标签示例 | 用途 | 模式 | 保留 |
|---------|------|------|------|
| `promo-traceflux-check-20260307` | 检查 PR 状态 | `run` | 7 天 |
| `promo-traceflux-submit-20260307` | 提交 PR | `run` | 30 天 |
| `promo-traceflux-search-20260307` | 搜索新列表 | `run` | 7 天 |

### 会话清理策略

**一次性会话** (`mode: "run"`):
- 任务完成后自动结束
- 会话历史保留 (可通过 `sessions_history` 查询)
- 建议定期清理 (>30 天)

**清理脚本**:
```python
# ~/.openclaw/promotions/cleanup-old-sessions.py
import subprocess
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=30)
# 列出所有 promo- 开头的会话
# 过滤出早于 cutoff 的
# 删除或归档
```

---

## 与主会话的交互

### 交互原则

1. **最小打扰** - 结果写入文件，用户主动查看
2. **异常才通知** - 只有错误/被拒才主动发消息
3. **汇总报告** - 定期 (每周) 汇总，非实时

### 交互模式

```
模式 A: 用户主动查询 (推荐)
  用户: "查看 traceflux 推广状态"
  助手: 读取 ~/.openclaw/promotions/traceflux/state/last-check-result.md
  助手: 返回报告内容

模式 B: 异常通知 (仅异常)
  推广会话: 检测到 PR 被拒
  推广会话: 发送消息到主会话
  主会话: "⚠️ PR #12345 被拒绝，原因：..."

模式 C: 每周汇总 (可选)
  每周日: 自动生成周报
  写入: ~/.openclaw/promotions/traceflux/logs/weekly-summary.md
  用户: 主动查看或推送到主会话
```

---

## 备份与恢复

### 备份策略

**方案 A: 独立 Git 仓库** (推荐)
```bash
cd /home/openclaw/.openclaw/promotions/
git init
git add traceflux/
git commit -m "Initial state"
# 推送到私有仓库
git remote add origin git@github.com:tracer-mohist/traceflux-promotion-state.git
git push -u origin main
```

**方案 B: 定期归档到项目**
```bash
# 每周执行
cp ~/.openclaw/promotions/traceflux/state/submissions.json \
   /home/openclaw/tracer/dev-repo/traceflux/.github/archive/submissions-20260307.json
cd /home/openclaw/tracer/dev-repo/traceflux/
git add .github/archive/
git commit -m "Archive promotion state 2026-03-07"
```

**方案 C: 不备份** (可接受)
- 推广状态不是关键数据
- 丢失后可从 GitHub 重新查询
- 适合初期阶段

### 恢复流程

```bash
# 从备份恢复
cd /home/openclaw/.openclaw/promotions/
git pull origin main

# 或从项目归档恢复
cp /home/openclaw/tracer/dev-repo/traceflux/.github/archive/submissions-20260307.json \
   ~/.openclaw/promotions/traceflux/state/submissions.json

# 或手动重建
# 1. 从 GitHub 查询所有 PR
# 2. 重新填充 state 文件
```

---

## 目录创建脚本

```bash
#!/bin/bash
# create-promotion-storage.sh
# 创建推广专用存储目录

PROJECT="traceflux"
BASE_DIR="/home/openclaw/.openclaw/promotions/$PROJECT"

# 创建目录结构
mkdir -p "$BASE_DIR/state"
mkdir -p "$BASE_DIR/logs"
mkdir -p "$BASE_DIR/drafts"
mkdir -p "$BASE_DIR/config"
mkdir -p "$BASE_DIR/archive"

# 创建初始状态文件
cat > "$BASE_DIR/state/submissions.json" << 'EOF'
{
  "meta": {
    "version": 1,
    "project": "traceflux",
    "createdAt": "$(date -Iseconds)",
    "lastUpdated": "$(date -Iseconds)"
  },
  "targets": {},
  "history": [],
  "stats": {
    "totalSubmitted": 0,
    "accepted": 0,
    "rejected": 0,
    "pending": 0
  },
  "rateLimit": {
    "maxPerWeek": 2,
    "submissionsThisWeek": 0,
    "weekStartsAt": "$(date -Iseconds)",
    "lastSubmissionAt": null
  }
}
EOF

# 创建目标配置
cat > "$BASE_DIR/config/targets.json" << 'EOF'
{
  "priority1": [
    {
      "repo": "frutik/awesome-search",
      "category": "Search Tools",
      "reason": "Direct category match"
    },
    {
      "repo": "vinta/awesome-python",
      "category": "Text Processing",
      "reason": "Most popular Python list"
    }
  ],
  "priority2": [],
  "blacklist": []
}
EOF

# 创建约束配置
cat > "$BASE_DIR/config/constraints.json" << 'EOF'
{
  "rateLimit": {
    "maxPerWeek": 2,
    "minDaysBetween": 7
  },
  "requirements": {
    "minStars": 30,
    "minAge": 14,
    "hasLicense": true
  },
  "autoSubmit": false,
  "requireConfirmation": true
}
EOF

echo "Created promotion storage for $PROJECT at $BASE_DIR"
```

---

## 决策记录

### 决策 1: 使用独立存储目录

**日期**: 2026-03-07  
**决策**: 采用方案二 (独立存储目录)

**理由**:
1. 推广是跨项目活动，需要集中管理
2. 日志量大，不应污染项目仓库
3. 配置可复用于其他项目
4. 易于清理和维护

**存储位置**: `~/.openclaw/promotions/<project>/`

---

### 决策 2: 状态文件不纳入项目 Git

**日期**: 2026-03-07  
**决策**: 状态文件存储在独立目录，不纳入项目 Git

**理由**:
1. 状态频繁变化，会产生大量 commits
2. 与项目代码无关
3. 可接受损失 (可从 GitHub 重建)

**备份方案**: 可选独立 Git 仓库或定期归档

---

### 决策 3: 日志独立存储

**日期**: 2026-03-07  
**决策**: 所有推广日志存储在独立目录

**理由**:
1. 日志量大 (每次检查都产生)
2. 与项目无关
3. 便于调试和审计
4. 不污染项目仓库

---

## 下一步行动

### 立即执行

- [ ] 创建目录结构 (`mkdir -p ~/.openclaw/promotions/traceflux/{state,logs,drafts,config}`)
- [ ] 创建初始状态文件
- [ ] 创建配置文件
- [ ] 测试手动触发流程

### 第一次推广

- [ ] 搜索目标 awesome lists
- [ ] 检查项目要求 (stars, age, license)
- [ ] 准备 PR 草稿
- [ ] 用户确认
- [ ] 提交 PR
- [ ] 记录到状态文件

### 后续优化

- [ ] 根据经验调整配置
- [ ] 考虑是否需要 Cron
- [ ] 建立归档流程
- [ ] 总结经验文档

---

## 相关文件

- `docs/PROMOTION-STRATEGY-DESIGN.md` - 策略设计 v1
- `docs/AWESOME-PROMOTION-DESIGN.md` - 技术设计
- `docs/OPENCLAW-AWESOME-TASK.md` - OpenClaw 任务指南

---

**设计原则**: 隔离、可复用、易维护  
**核心理念**: 推广是独立活动，与项目开发分离

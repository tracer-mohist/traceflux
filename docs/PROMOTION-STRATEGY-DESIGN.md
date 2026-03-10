<!-- docs/PROMOTION-STRATEGY-DESIGN.md -->
# traceflux Awesome List 推广策略设计

**日期**: 2026-03-07  
**状态**: 设计草案  
**作者**: Tracer

---

## 核心约束

### 1. 隔离原则

**问题**: HEARTBEAT.md 在主会话执行，会污染主会话历史

**约束**:
- ✅ 推广任务必须隔离
- ✅ 不污染主会话记忆
- ✅ 不影响主会话的连续性

### 2. 人工参与原则

**问题**: 推广需要判断和决策，不能完全自动化

**约束**:
- ✅ 提交前需要用户确认
- ✅ 被拒后需要人工分析原因
- ✅ 维护者反馈需要人工回复

### 3. 速率限制原则

**问题**: 过度提交会被视为 spam

**约束**:
- ✅ 最多 2 个提交/周
- ✅ 至少间隔 7 天
- ✅ 尊重维护者决定

---

## 方案对比

### 方案 A: 手动触发 + 独立会话

```
用户主动发起:
  "检查 traceflux awesome list 状态"
      │
      ▼
sessions_spawn (独立子代理)
  - 加载状态文件
  - 检查 PR 状态
  - 更新记录
  - 返回结果
      │
      ▼
主会话接收报告
  - 用户查看结果
  - 用户决定下一步
```

**优点**:
- ✅ 完全隔离 (独立会话日志)
- ✅ 用户完全控制
- ✅ 不污染主会话
- ✅ 简单，无需额外配置

**缺点**:
- ❌ 需要用户记住检查
- ❌ 可能忘记定期检查

**适用场景**:
- 推广初期 (提交少，频率低)
- 用户希望完全控制
- 不需要精确时间调度

---

### 方案 B: 专用 Cron Job + 通知

```
Cron 配置 (~/.openclaw/cron/jobs.json):
{
  "jobs": [
    {
      "name": "traceflux-awesome-check",
      "schedule": "0 10 */3 * *",  // 每 3 天 10:00
      "command": "sessions_spawn --label awesome-check --task '...'",
      "notify": true
    }
  ]
}

Cron 触发 → 独立会话执行 → 结果写入文件 → 通知用户
```

**优点**:
- ✅ 完全自动化
- ✅ 精确时间控制
- ✅ 不依赖用户记忆
- ✅ 隔离执行

**缺点**:
- ❌ 需要配置 Cron (当前为空)
- ❌ 通知机制需要额外开发
- ❌ 过度自动化 (推广需要人工判断)

**适用场景**:
- 推广成熟期 (流程稳定)
- 提交量大 (需要自动化)
- 用户希望"设置后忘记"

---

### 方案 C: 专用会话 + 外部提醒

```
专用会话 (持久):
  - 会话标签: "traceflux-promotion"
  - 会话模式: session (持久)
  - 会话职责: 跟踪推广进度

外部提醒 (非 OpenClaw):
  - 手机日历提醒 (每 3 天)
  - 或 Todo 应用提醒
  - 或物理便签

提醒 → 用户 → 向专用会话发消息 → 执行检查
```

**优点**:
- ✅ 上下文隔离 (专用会话)
- ✅ 推广历史集中记录
- ✅ 提醒机制灵活
- ✅ 不污染主会话

**缺点**:
- ❌ 需要维护专用会话
- ❌ 外部提醒需要额外工具

**适用场景**:
- 中长期推广 (持续数月)
- 用户习惯用 Todo/日历
- 希望推广历史独立存档

---

### 方案 D: 混合方案 (推荐)

```
阶段 1: 手动触发 (当前 - 第 1 个月)
  - 用户主动发起 sessions_spawn
  - 建立流程和经验
  - 记录到状态文件

阶段 2: 半自动 (第 2-3 个月)
  - 添加简单 Cron (只检查，不提交)
  - 检查结果写入文件
  - 用户查看后决定是否提交

阶段 3: 全自动 (3 个月后，可选)
  - 如果流程稳定，考虑自动化提交
  - 保留人工确认环节
  - 异常情况下人工介入
```

**优点**:
- ✅ 渐进式，风险可控
- ✅ 早期人工参与 (学习流程)
- ✅ 后期可自动化 (减少负担)
- ✅ 随时可回退到手动

**缺点**:
- ❌ 需要阶段性调整
- ❌ 需要记录经验教训

---

## 推荐方案：方案 D (混合方案)

### 阶段 1: 手动触发 (立即开始)

**配置**: 无需额外配置

**工作流**:
```
用户 (主会话)
  │
  │ "检查 awesome list 状态"
  ▼
sessions_spawn (独立子代理)
  runtime: "subagent"
  label: "traceflux-awesome-check"
  mode: "run"
  task: |
    cd /home/openclaw/tracer/dev-repo/traceflux
    python scripts/check-awesome-status.py
    报告状态变化
  │
  │ 返回结果
  ▼
用户查看报告 → 决定下一步
```

**状态跟踪**:
- 文件: `.github/awesome-submissions.json`
- Git 版本控制 (每次提交后 commit)
- 手动检查频率: 用户决定 (建议 2-3 天)

**优点**:
- 零配置
- 完全隔离
- 用户学习流程
- 建立经验

---

### 阶段 2: 半自动 (1-2 个月后)

**触发条件**:
- 已提交 3+ 个 awesome lists
- 流程已稳定
- 用户希望减少手动操作

**配置**: 添加 Cron Job

```json
// ~/.openclaw/cron/jobs.json
{
  "version": 1,
  "jobs": [
    {
      "id": "traceflux-awesome-check",
      "name": "Traceflux Awesome List Status Check",
      "schedule": "0 10 */3 * *",
      "enabled": true,
      "command": "sessions_spawn",
      "params": {
        "runtime": "subagent",
        "label": "traceflux-awesome-check",
        "mode": "run",
        "task": "cd /home/openclaw/tracer/dev-repo/traceflux && python scripts/check-awesome-status.py"
      },
      "notify": {
        "enabled": true,
        "method": "file",
        "path": ".github/awesome-check-result.md"
      }
    }
  ]
}
```

**工作流**:
```
Cron (每 3 天 10:00)
  │
  ▼
sessions_spawn (独立子代理)
  - 检查 PR 状态
  - 更新状态文件
  - 写入结果文件
  │
  ▼
.github/awesome-check-result.md
  - 检查结果
  - 状态变化
  - 建议操作

用户 (主动查看)
  - 读取结果文件
  - 决定下一步操作
```

**关键设计**:
- Cron **只检查**，不提交
- 提交仍需用户确认
- 结果写入文件，不发消息 (避免骚扰)
- 用户主动查看 (控制节奏)

---

### 阶段 3: 全自动 (可选，3 个月后)

**触发条件**:
- 已提交 10+ 个 awesome lists
- 接受率 > 50%
- 流程完全稳定
- 用户明确授权

**配置**: 扩展 Cron Job

```json
{
  "jobs": [
    {
      "id": "traceflux-awesome-submit",
      "name": "Traceflux Awesome List Auto-Submit",
      "schedule": "0 14 * * 1",  // 周一 14:00
      "enabled": true,
      "command": "sessions_spawn",
      "params": {
        "runtime": "subagent",
        "label": "traceflux-awesome-submit",
        "mode": "run",
        "task": "..."
      },
      "constraints": {
        "maxPerWeek": 2,
        "minDaysBetween": 7,
        "requireStars": 50,
        "requireAge": 30,
        "autoConfirm": false  // 仍需确认
      }
    }
  ]
}
```

**关键约束**:
- 仍保留人工确认 (`autoConfirm: false`)
- 严格速率限制
- 自动检查项目要求 (stars, age)
- 异常情况人工介入

---

## 状态管理设计

### 核心状态文件

**位置**: `traceflux/.github/awesome-submissions.json`

**结构**:
```json
{
  "version": 1,
  "createdAt": "2026-03-07T20:30:00+08:00",
  "lastUpdated": "2026-03-07T20:30:00+08:00",
  
  "searchProgress": {
    "vinta/awesome-python": {
      "searchedAt": "2026-03-07T20:30:00+08:00",
      "found": true,
      "category": "Text Processing",
      "hasContributing": true,
      "notes": "Most popular Python list"
    }
  },
  
  "submissions": [
    {
      "id": "awesome-python-001",
      "repo": "vinta/awesome-python",
      "category": "Text Processing",
      "submittedAt": "2026-03-07T20:30:00+08:00",
      "prNumber": 12345,
      "prUrl": "https://github.com/vinta/awesome-python/pull/12345",
      "status": "pending",
      "statusHistory": [
        {"status": "pending", "timestamp": "2026-03-07T20:30:00+08:00"}
      ],
      "notes": "Awaiting review"
    }
  ],
  
  "blacklist": [
    {
      "repo": "some-repo/awesome-list",
      "reason": "Rejected - not enough stars",
      "cooldownUntil": "2026-06-07"
    }
  ],
  
  "stats": {
    "totalSearched": 3,
    "totalSubmitted": 1,
    "accepted": 0,
    "rejected": 0,
    "pending": 1
  },
  
  "rateLimit": {
    "maxPerWeek": 2,
    "minDaysBetween": 7,
    "lastSubmission": "2026-03-07T20:30:00+08:00"
  }
}
```

### Git 版本控制

**原则**: 状态文件纳入 Git 管理

**原因**:
- 历史记录可追溯
- 防止意外丢失
- 跨会话连续性
- 可回滚到任意时间点

**Commit 时机**:
```bash
# 每次状态变化后
git add .github/awesome-submissions.json
git commit -m "chore: update awesome submission status
  - vinta/awesome-python: pending → accepted"
git push
```

---

## 会话隔离设计

### 会话标签规范

**格式**: `traceflux-<任务类型>`

| 标签 | 用途 | 模式 |
|------|------|------|
| `traceflux-awesome-check` | 检查 PR 状态 | `run` (一次性) |
| `traceflux-awesome-submit` | 准备/提交 PR | `run` (一次性) |
| `traceflux-awesome-search` | 搜索新列表 | `run` (一次性) |
| `traceflux-promotion` | 长期跟踪 (可选) | `session` (持久) |

### 会话清理策略

**一次性会话** (`mode: "run"`):
- 任务完成后自动结束
- 会话历史保留 (可查询)
- 不占用资源

**持久会话** (`mode: "session"`, 可选):
- 长期保持活跃
- 集中所有推广上下文
- 需要时清理

**推荐**: 使用一次性会话，无需清理

---

## 通知策略

### 原则

1. **不主动打扰** - 结果写入文件，用户主动查看
2. **异常才通知** - 只有错误/被拒才主动提醒
3. **汇总报告** - 定期 (每周) 汇总，非实时

### 通知方式对比

| 方式 | 优点 | 缺点 | 推荐 |
|------|------|------|------|
| 主会话消息 | 即时可见 | 打扰用户 | ❌ |
| 写入文件 | 不打扰，用户主动查看 | 可能被忽略 | ✅ (默认) |
| 邮件通知 | 正式，可追踪 | 配置复杂 | ⚠️ (可选) |
| 外部推送 | 即时，跨设备 | 需要额外工具 | ❌ |

### 推荐方案

**默认**: 写入文件
```
.github/awesome-check-result.md
  - 检查时间
  - 状态变化
  - 建议操作

用户主动查看 (如每天一次)
```

**异常**: 主会话消息
```
⚠️ traceflux 推广异常

PR #12345 被拒绝
原因: 项目 stars 不足 (当前 45, 要求 50)

建议: 达到 50 stars 后重试
```

---

## 风险评估

### 风险矩阵

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 被视为 spam | 中 | 高 | 严格速率限制，人工确认 |
| 重复提交 | 低 | 中 | 状态文件跟踪 |
| 状态文件丢失 | 低 | 中 | Git 版本控制 |
| 会话污染 | 低 | 低 | 独立会话执行 |
| 过度自动化 | 中 | 中 | 保留人工确认 |
| 忘记检查 | 高 | 低 | 外部提醒 (日历) |

### 缓解措施汇总

1. **速率限制** - 代码 + 配置双重限制
2. **人工确认** - 所有提交需用户批准
3. **Git 备份** - 状态文件版本控制
4. **独立会话** - 不污染主会话
5. **渐进自动化** - 从手动到半自动到自动

---

## 成功指标

### 短期 (1 个月)

- [ ] 完成 3-5 个高质量提交
- [ ] 接受率 > 50%
- [ ] 建立稳定流程
- [ ] 状态文件完善

### 中期 (3 个月)

- [ ] 完成 10-15 个提交
- [ ] 接受率 > 60%
- [ ] 半自动化运行
- [ ] star 增长 +30%

### 长期 (6 个月)

- [ ] 覆盖 20+ awesome lists
- [ ] 接受率 > 70%
- [ ] 全自动 (可选)
- [ ] star 增长 +100%

---

## 决策记录

### 决策 1: 不使用 HEARTBEAT.md

**日期**: 2026-03-07  
**决策**: 避免使用 HEARTBEAT.md 机制

**理由**:
1. HEARTBEAT 在主会话执行，会污染历史
2. 推广任务需要隔离上下文
3. HEARTBEAT 设计用于健康检查，不是任务调度
4. 推广需要人工判断，不适合自动轮询

**替代方案**: sessions_spawn + 独立会话

---

### 决策 2: 采用混合方案 (阶段式)

**日期**: 2026-03-07  
**决策**: 从手动开始，渐进自动化

**理由**:
1. 早期需要学习流程
2. 建立经验后再自动化
3. 风险可控，随时回退
4. 符合"简单优先"原则

**阶段**:
- 阶段 1: 手动触发 (立即)
- 阶段 2: 半自动 (1-2 个月后)
- 阶段 3: 全自动 (可选，3 个月后)

---

### 决策 3: 状态文件 Git 管理

**日期**: 2026-03-07  
**决策**: `.github/awesome-submissions.json` 纳入 Git

**理由**:
1. 防止数据丢失
2. 历史记录可追溯
3. 跨会话连续性
4. 支持回滚

---

## 下一步行动

### 立即 (阶段 1)

- [x] 创建状态文件
- [x] 创建检查脚本
- [x] 创建设计文档
- [ ] 手动提交第一个 PR (frutik/awesome-search)
- [ ] 记录提交流程和经验

### 1-2 个月后 (阶段 2)

- [ ] 评估流程稳定性
- [ ] 配置 Cron Job (只检查)
- [ ] 建立外部提醒 (日历)
- [ ] 继续手动提交

### 3 个月后 (阶段 3, 可选)

- [ ] 评估自动化需求
- [ ] 如需要，配置自动提交 (保留确认)
- [ ] 优化速率限制
- [ ] 总结经验文档

---

## 相关文件

- `docs/AWESOME-PROMOTION-DESIGN.md` - 初始设计
- `docs/OPENCLAW-AWESOME-TASK.md` - OpenClaw 任务指南
- `.github/awesome-submissions.json` - 状态文件
- `scripts/check-awesome-status.py` - 检查脚本

---

**设计原则**: 隔离、人工控制、渐进自动化  
**核心理念**: 工具服务于人，不是人服务于工具

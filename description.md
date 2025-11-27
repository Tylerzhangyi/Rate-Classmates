# 售货机商品评价平台 – 功能说明

## 使用人群
不同学校的学生可以通过这个网站去对不同学校售货机中的商品进行打分.

## 被评对象
分布在不同学校校园内的售货机商品（饮料、零食、日用品等），可直接按学校、品牌、品类、容量以及渠道合作方等维度浏览，无需关注具体机器。

## 评分体系
- 主等级：五档语义等级 `夯 > 顶级 > 人上人 > NPC > 拉完了`。
- 多维评分：`口味/品质`、`性价比`、`包装体验`、`供应稳定性` 四个 1–10 分维度。
- 标签体系：运营方维护的标签库（如“解馋”“低糖”“季节限定”），投票时用户仅需勾选。

## 额外/可选功能
- 排行榜：Top 10 综合榜、新品榜、地区/学校榜，支持按周期（周/月/季度）自动生成并导出。
- 徽章体系：授予商品或学校的称号，如“年度口碑王”“最具性价比零食”“补货最及时学校”。
- 搜索与筛选：按学校、品牌、品类、地区、价格区间等条件检索。
- 评分排序：按综合等级、多维平均、最近 30 天变化率等维度排序。

## 交互特性
- 校方/合作服务商后台可批量导出评分、配置标签、设置榜单周期并定义徽章条件。


---

## ER 模型概览
平台围绕“学生为不同学校售货机商品打分”这一场景，仅保留支撑评分、标签、徽章、榜单与筛选的必要数据结构。核心实体如下：

| 实体 | 关键字段 | 说明 |
| --- | --- | --- |
| Product | product_id (PK)、名称、品牌、类别、规格、上市日期、是否季节限定 | 售货机商品本体 |
| School | school_id (PK)、学校名称、城市、国家、类型（大学/高中等）、合作方 | 校园实体 |
| SchoolProduct | school_product_id (PK)、school_id (FK)、product_id (FK)、售价 | 学校与商品的关联与定价 |
| RatingSubmission | rating_id (PK)、school_product_id (FK)、等级、多维分、标签数组 | 学生端评分记录（无账号，仅匿名采集） |
| Tag | tag_id (PK)、名称、描述 | 标签库 |
| RatingTag | rating_tag_id (PK)、rating_id (FK)、tag_id (FK) | 评分与标签的 M:N |
| Badge | badge_id (PK)、名称、描述、类型（商品/学校）、评选规则 | 徽章定义 |
| ProductBadge | product_badge_id (PK)、product_id (FK)、badge_id (FK)、period | 商品获徽 |
| SchoolBadge | school_badge_id (PK)、school_id (FK)、badge_id (FK)、period | 学校获徽 |
| Leaderboard | leaderboard_id (PK)、名称、类型、计算逻辑 | 榜单定义 |
| LeaderboardEntry | entry_id (PK)、leaderboard_id (FK)、product_id (FK)、rank、score | 榜单条目，记录商品在各榜单中的名次 |

### 基数关系
- `School` 1:N `SchoolProduct`，`Product` 1:N `SchoolProduct`。
- `SchoolProduct` 1:N `RatingSubmission`。
- `RatingSubmission` M:N `Tag`（通过 `RatingTag`）。
- `Badge` 1:N `ProductBadge` / `SchoolBadge`。
- `Leaderboard` 1:N `LeaderboardEntry`，`Product` 1:N `LeaderboardEntry`；可扩展以学校为主体的榜单。



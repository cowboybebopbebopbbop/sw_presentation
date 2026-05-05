# SimpleWine Studio — Конкурентный аудит

> **Назначение этой папки:** полный конкурентный аудит системы SimpleWine Studio (репозиторий `cowboybebopbebopbbop/sw`) против 7 конкурентов по 22 критериям, разбитый на 8 тематических блоков. Подготовлено для защиты пилота 170-250к₽/мес перед топ-менеджментом, контент-командой, IT-директором и финдиром SimpleWine.

---

## Как пользоваться (для нового AI-агента)

1. **Начни с** [`00_CONTEXT.md`](./00_CONTEXT.md) — там вся фактура: что за система, что за встреча, кто такая Алина, какие возражения, что за конкуренты, какие модели используются.
2. **Затем** [`09_FINAL_VERDICT.md`](./09_FINAL_VERDICT.md) — сводный итог по всем 8 блокам + готовые talking points.
3. **Глубже** — конкретные блоки `01_…` … `08_…` по нужной теме.
4. **Если задают конкретный вопрос** (цена, безопасность, vendor) — иди прямо в соответствующий блок, там матрица + вердикты + честные оговорки + главный аргумент.

## Структура

| Файл | Содержание |
|---|---|
| [`00_CONTEXT.md`](./00_CONTEXT.md) | Контекст: система, встреча, конкуренты, модели, рамка аудита |
| [`01_PERFORMANCE.md`](./01_PERFORMANCE.md) | Блок 1: скорость, объём, A/B, batch SKU |
| [`02_QUALITY_CONTROL.md`](./02_QUALITY_CONTROL.md) | Блок 2: детерминированный валидатор, compliance, consistency |
| [`03_CUSTOMIZATION_BRAND.md`](./03_CUSTOMIZATION_BRAND.md) | Блок 3: ToV, лексикон, расширяемость, vendor lock-in |
| [`04_COST_ECONOMICS.md`](./04_COST_ECONOMICS.md) | Блок 4: TCO, токены, декомпозиция тарифа, сценарии пилота |
| [`05_SECURITY_COMPLIANCE.md`](./05_SECURITY_COMPLIANCE.md) | Блок 5: где данные, PII, audit-trail, чеклист для IT |
| [`06_PROCESS_KNOWLEDGE.md`](./06_PROCESS_KNOWLEDGE.md) | Блок 6: bus factor, knowledge retention, git как корп-знание |
| [`07_INTEGRATION_E2E.md`](./07_INTEGRATION_E2E.md) | Блок 7: production runtime vs chat surface, end-to-end |
| [`08_VENDOR_RISK.md`](./08_VENDOR_RISK.md) | Блок 8: lock-in, санкции, multi-model, on-prem |
| [`09_FINAL_VERDICT.md`](./09_FINAL_VERDICT.md) | Сводный вердикт + talking points + сценарии пилота |

## Шкала вердиктов

- 🟢 **выиграли** — у нас явное преимущество
- 🟡 **ничья** — конкурент способен на сопоставимое
- 🔴 **проиграли** — конкурент объективно сильнее
- ⚪ **не применимо** — критерий не относится к категории

## Конкуренты (везде одни и те же 7)

1. **ChatGPT web/Plus** — голый чат
2. **ChatGPT Custom GPT** — кастом с загруженными файлами + Actions
3. **ChatGPT Projects** — проекты с общей памятью (+ ChatGPT Enterprise упоминается отдельно в Блоке 5)
4. **Claude.ai / Pro** — голый чат Anthropic
5. **Claude Projects** — проекты с системным промптом и файлами
6. **AlpinaGPT** — российский агрегатор-маршрутизатор к иностранным LLM (199₽/мес личный, 13.2к₽/мес business)
7. **Yandex GPT / GigaChat** — российские LLM

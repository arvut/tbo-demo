# tbo-demo — демо-лендинг TBO Treuhand AG (Цюрих)

Наташа, привет! 👋 Ты была в отъезде, а лид TBO горячий (встреча Alex×Spreiter **15.07**), поэтому
первую версию лендинга собрали мы твоим скилом `landing-page-fiduciary`. **Правь всё, что захочешь** —
это черновик под твою руку. Репо и Pages настроены как у `aar-demo`/`mdv-demo`, ты — коллаборатор с
правом записи.

## Что это

Партнёрский демо-лендинг **бухгалтерии в реальном времени + внешнего финдиректора** для клиентов
фидуциарии **TBO Treuhand AG** (классический дом Treuhand + Revision, Цюрих, с 1962). Обращён к
**КЛИЕНТУ** фидуциарии (владелец компании, покупающий бухгалтерию), Sie-форма. Сделан в **их** стиле
(смотрел живой tbo.ch: верхнее белое меню, лого «tbo» слева, hero = фото + матовая стеклянная
карточка, navy `#002060`, скруглённые карточки, круглые фото-иконки — НЕ копия AAR/MDV).

- **Live (GitHub Pages):** https://arvut.github.io/tbo-demo/
- Язык: **только немецкий** (швейцарский Hochdeutsch, `ss` не `ß`). Мультиязык (FR/IT/EN + скрытый
  RU) сделаем потом нашим агентом-переводчиком — тебе не надо.
- Логотип и фото персон (Spreiter/Shahini) — реальные, из папки проекта TBO.
  hero-фото и Цюрих — Unsplash (реальный сток, не ИИ), как в твоём скиле.

## 🔒 Два правила канона — НЕ менять

1. **Формула позиционирования — дословно** (секция «Leitsatz», голубая полоса под hero):
   > «Der klassische Treuhänder ist der geteilte Buchhalter der KMU. Der Treuhänder im
   > Arvut-Netzwerk ist zusätzlich ihr **externer CFO** — für KMU wie für grössere Unternehmen.»
   Никогда «shared CFO» / «geteilter CFO» / «fraktionaler CFO». «Externer CFO» / «Virtual CFO»
   (название пакета) — ок.
2. **Ноль про DAP / механику протокола.** Можно только РЕЗУЛЬТАТ («Solvenz und echte Marge in
   Echtzeit»), но слова DAP / Digital Accounting Protocol / названия состояний — НИКОГДА (это
   NDA-only). Профиль TBO — Treuhand + Revision, с 1962, НЕ «IT/Marketing», НЕ «Erbschaft/Nachfolge».

Структура-образец текстов (как договаривались) — **https://cs.arvut.ch/de/** (Schreiber-лендинг).
Цифры на лендинге — из маркет-исследования TBO (`arvut.ch/tbo/marktstudie`, код 1515): Vollkosten
Buchhalter Zürich ≈ CHF 110'000, тарифы 18k/36k/60k, пилот CHF 1'000/Mandat (anrechenbar).

## Структура файла

Всё в одном `index.html` (инлайн-стили, как у твоих демо). Секции по порядку:
Hero → Was sich ändert (Heute/Mit TBO) → **Leitsatz (формула)** → Leistungen (6) → Darum lohnt es
sich (Kennzahlen) → Pakete (3 тарифа) → Arbeitsweise (3 шага) → Akzent-Banner (Zürich) → Ihr
Finanzteam (Spreiter/Shahini) → Region → Kontakt (демо-форма) → Footer (кредит Arvut зелёным).

- Шрифты локальные (`assets/fonts/`, Manrope заголовки + Inter текст) — Google Fonts `@import`
  не успевает в headless, поэтому woff2 лежат в репо.
- Дизайн-токены — в `:root` (навигируй по `--navy`, `--soft`, `--band`, `--radius`).
- Картинки — `assets/img/`. При замене меняй `?v=N` в HTML (иначе CDN отдаёт старое).

## Деплой

Пуш в `main` → GitHub Actions (`.github/workflows/pages.yml`) автоматически публикует на Pages.
Проверить: https://arvut.github.io/tbo-demo/

## ⛔ Не публиковать на tbo.arvut.ch и не слать партнёру

Прод-домен `tbo.arvut.ch` (контейнер + GCP-proxy, как cs-demo) поднимем **только после твоих правок
и OK Alex**. Магическую ссылку/лендинг партнёру (TBO) до этого НЕ шлём — гейт client_email_approval.

Спасибо! Вопросы — Alex.

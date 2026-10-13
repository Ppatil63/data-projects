# Insights — Retail Sales (Sample Superstore, 2014–2017)

Every number below is computed by `etl.py` / `analysis.sql` from the actual
dataset (9,994 order lines, 5,009 orders) and stored in `outputs/kpis.txt`.

- **The business is healthy overall, but barely:** $2,297,200.86 in sales
  produced $286,397.02 in profit — a 12.47% margin across four years.
- **Furniture is the problem category.** It is the #2 category by sales
  ($741,999.80) yet returns only $18,451.27 profit — a 2.49% margin, versus
  17.40% for Technology ($145,454.95 profit on $836,154.03 sales) and ~17%
  for Office Supplies ($122,490.80). Furniture discounting and product mix
  are where margin leaks.
- **Discounts over 20% destroy profit.** Order lines with no discount
  average +$66.90 profit; lines discounted 21–40% average **−$77.86**, and
  lines discounted over 40% average **−$106.71**. 1,393 lines (460 + 933)
  were sold at discounts deep enough to lose money on average.
- **The West region carries profitability.** West generated the most profit
  ($108,418.45), while Central made the least ($39,706.36) despite $501,239.89
  in sales — Central is a high-revenue, low-margin region worth a pricing
  review.
- **Growth is real and accelerating.** Sales rose from $484,247.50 in 2014
  to $733,215.26 in 2017 (+51%), and profit rose every year ($49,543.97 →
  $93,439.27). The single biggest month was November 2017 at $118,447.83 —
  a clear holiday-season peak.
- **A few products dominate both ends.** The Canon imageCLASS 2200 copier
  alone contributed $25,199.93 profit. At the other end, the Cubify CubeX 3D
  Printer (Double Head) lost $8,879.97 and the Lexmark MX611dhe lost
  $4,589.97 — candidates for repricing or delisting.

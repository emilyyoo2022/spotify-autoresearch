Week 3 Reflection

This week, I focused on running a real AutoResearch loop on my Spotify popularity prediction project. The goal was not to improve performance as much as possible, but to make sure the loop actually runs end-to-end with clear boundaries and consistent evaluation.

I restricted the agent to only modifying model.py, while keeping the dataset, data split, and evaluation metric (RMSE) fixed. This ensured that all experiments remained comparable. Each run was executed using the same command and evaluated on the same validation set.

The agent performed well in quickly testing different model types and reporting results. It was able to run experiments end-to-end, return RMSE and R², and make clear keep or discard decisions. For example, it identified that Random Forest significantly outperformed the baseline linear model, reducing RMSE from about 22 to around 15.

However, the agent also showed limitations. It required very explicit instructions to stay within scope and not modify protected parts of the pipeline. Additionally, not all model changes were useful—Ridge regression produced identical results to the baseline, and some models like gradient boosting performed worse with default settings. This showed that the agent does not inherently know which changes are meaningful without guidance.

One key insight from this week was that model choice matters much more than small parameter tweaks at this stage. Switching from linear models to tree-based models had a large impact, while increasing the number of trees in Random Forest only produced marginal improvements and significantly increased runtime. This suggests that future improvements will likely come from better feature engineering rather than simply increasing model complexity.

Overall, the most important outcome was building a working, controlled loop where each experiment is interpretable and comparable. Even though performance is not fully optimized, the structure is now in place for more systematic experimentation going forward.
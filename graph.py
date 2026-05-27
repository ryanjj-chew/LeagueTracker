import pandas as pd
import seaborn as sns
import matplotlib, matplotlib.pyplot as plt
matplotlib.use("Agg")

class Graph():
    def __init__(self):
        sns.set_theme(style="darkgrid", palette="deep", context="talk")

    def timeline_graph(self, df, match_id):
        fig, axes = plt.subplots(1, 2, figsize=(12,5))

        # Gold 
        sns.lineplot(data=df[df["stat"] == "gold"], x="minute", y="value", hue="team", ax=axes[0])
        axes[0].set_title("Gold")

        # XP
        sns.lineplot(data=df[df["stat"] == "xp"], x="minute", y="value", hue="team", ax=axes[1])
        axes[1].set_title("XP")
        axes[1].legend().remove()

        # Declare the graphs' style and range
        axes[0].tick_params(colors="white")
        axes[0].xaxis.label.set_color("white")
        axes[0].yaxis.label.set_color("white")
        axes[0].title.set_color("white")
        axes[0].set_xlabel("Minute")
        axes[0].set_ylabel("Gold")
        axes[0].set_xlim(0)
        axes[0].set_ylim(0)

        axes[1].tick_params(colors="white")
        axes[1].xaxis.label.set_color("white")
        axes[1].yaxis.label.set_color("white")
        axes[1].title.set_color("white")
        axes[1].set_xlabel("Minute")
        axes[1].set_ylabel("XP")
        axes[1].set_xlim(0)
        axes[1].set_ylim(0)

        axes[0].legend(title="Team")

        fig.tight_layout()
        sns.despine()

        filename = f"static/graphs/{match_id}.png"
        plt.savefig(filename, transparent=True, bbox_inches="tight")
        plt.close()

        return f"graphs/{match_id}.png"
    
    def timeline_diff_graph(self, df, match_id):
        fig, axes = plt.subplots(2, 1, figsize=(12,8), sharex=True)
        
        # Gold Differential
        df["gold_diff"] = df["player_team_gold"] - df["enemy_team_gold"]
        sns.lineplot(data=df, x="minute", y="gold_diff", ax = axes[0], color="orange")
        max_val = max(abs(df["gold_diff"].max()), abs(df["gold_diff"].min())) * 1.1
        

        # XP Differential
        df["xp_diff"] = df["player_team_xp"] - df["enemy_team_xp"]
        sns.lineplot(data=df, x="minute", y="xp_diff", ax=axes[1], color="green")
        max_val = max(abs(df["xp_diff"].max()), abs(df["xp_diff"].min())) * 1.1
        
        # Declare the graphs' style and range
        axes[0].set_title("Gold Differential")
        axes[0].tick_params(colors="white")
        axes[0].xaxis.label.set_color("white")
        axes[0].yaxis.label.set_color("white")
        axes[0].title.set_color("white")
        axes[0].set_ylim(-max_val,max_val)
        axes[0].set_xlim(0)
        axes[0].set_xlabel("Minute")
        axes[0].set_ylabel("Gold")
        axes[0].axhline(0, linestyle="--", color="grey")

        axes[1].set_title("XP Differential")
        axes[1].tick_params(colors="white")
        axes[1].xaxis.label.set_color("white")
        axes[1].yaxis.label.set_color("white")
        axes[1].title.set_color("white")
        axes[1].set_ylim(-max_val,max_val)
        axes[1].set_xlim(0)
        axes[1].set_xlabel("Minute")
        axes[1].set_ylabel("XP")
        axes[1].axhline(0,linestyle="--", color="grey")

        fig.tight_layout()
        sns.despine()

        filename = f"static/graphs/{match_id}_diff.png"
        plt.savefig(filename, transparent=True, bbox_inches="tight")
        plt.close()
        
        return f"graphs/{match_id}_diff.png"
    
    def timeline_cs_graph(self, df, match_id):
        fig, ax = plt.subplots(figsize=(10,5))

        # Creep Score (CS) Graph
        sns.lineplot(data=df, x="minute", y="cs", ax=ax)

        # Declare the graph's style and range
        ax.set_title("Self CS Over Time")
        ax.set_xlabel("Minute")
        ax.set_ylabel("CS")
        ax.set_xlim(0)
        ax.set_ylim(0)
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        sns.despine()
        
        filename = f"static/graphs/{match_id}_cs.png"
        plt.savefig(filename, transparent=True, bbox_inches="tight")
        plt.close()
        
        return f"graphs/{match_id}_cs.png"
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import statistics

# --- USER INPUT ---
# Games
while True:
    try:
        games = int(input("How many games do you want to run? "))
        if games <= 0:
            print("Please enter a positive number.")
        else:
            break
    except ValueError:
        print("Please enter a valid whole number.")

# Strategy
strategies = ["random", "binary", "worst"]
while True:
    strategy = input(f"Choose strategy ({', '.join(strategies)}): ").strip().lower()
    if strategy in strategies:
        break
    else:
        print("Invalid strategy. Try again.")

# --- GAME LOOP ---
all_guess_counts = []

for _ in range(games):
    Min = 1
    Max = 100
    guess_count = 1
    HiddenNum = random.randint(Min, Max)

    if strategy == "random":
        Num = random.randint(Min, Max)
    elif strategy == "binary":
        Num = (Min + Max) // 2
    elif strategy == "worst":
        Num = Max  # Start with worst guess

    if Num > HiddenNum:
        response = "lower"
    elif Num < HiddenNum:
        response = "higher"
    else:
        response = "yes"

    while response in ["lower", "higher"]:
        if response == "lower":
            Max = Num - 1
        elif response == "higher":
            Min = Num + 1

        if Min > Max:
            break  # Inconsistent state

        guess_count += 1

        if strategy == "random":
            Num = random.randint(Min, Max)
        elif strategy == "binary":
            Num = (Min + Max) // 2
        elif strategy == "worst":
            Num = Max if HiddenNum < Num else Min  # Always guess the end of range

        if Num > HiddenNum:
            response = "lower"
        elif Num < HiddenNum:
            response = "higher"
        else:
            response = "yes"

    if response == "yes":
        all_guess_counts.append(guess_count)

# --- STATS + PLOT ---
if all_guess_counts:
    min_guesses = min(all_guess_counts)
    max_guesses = max(all_guess_counts)
    avg_guesses = sum(all_guess_counts) / len(all_guess_counts)
    std_dev = statistics.stdev(all_guess_counts)

    print("\n🎯 Final Score Summary 🎯")
    print(f"Games played: {games}")
    print(f"Strategy used: {strategy}")
    print(f"Minimum guesses: {min_guesses}")
    print(f"Maximum guesses: {max_guesses}")
    print(f"Average guesses: {avg_guesses:.2f}")
    print(f"Standard deviation (σ): {std_dev:.2f}")

    # Histogram
    plt.hist(
        all_guess_counts,
        bins=range(min_guesses, max_guesses + 2),
        edgecolor='black',
        alpha=0.7,
        density=True
    )

    # Format y-axis
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))

    # Stats lines
    plt.axvline(avg_guesses, color='blue', linestyle='dashed', linewidth=2, label=f'Mean: {avg_guesses:.2f}')
    plt.axvline(min_guesses, color='red', linestyle='dotted', linewidth=2, label=f'Min: {min_guesses}')
    plt.axvline(max_guesses, color='green', linestyle='dotted', linewidth=2, label=f'Max: {max_guesses}')
    plt.axvline(avg_guesses + std_dev, color='purple', linestyle='dashdot', linewidth=2, label=f'+1σ')
    plt.axvline(avg_guesses - std_dev, color='purple', linestyle='dashdot', linewidth=2, label=f'-1σ')

    # Titles and legend
    plt.title("Distribution of Guesses per Game")
    plt.suptitle(f"Games played: {games} — Strategy: {strategy}", fontsize=10, y=0.94, color='gray')
    plt.xlabel("Number of Guesses")
    plt.ylabel("Percentage of Games")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

else:
    print("No valid games were completed.")
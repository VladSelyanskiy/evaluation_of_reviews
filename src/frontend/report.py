# python
import os
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# 3rd parties
from mdutils.mdutils import MdUtils
from markdown_pdf import MarkdownPdf, Section
from statistics import mean, quantiles


# REPORT CLASS
# This class provides a short report on
# .JSON file of reviews with ratings.
# Makes .PDF and .MD files.


class Report:

    def get_summary(path_to_dir: str, file_name: str) -> str:
        """
        Dummy summary function
        Change to a real one
        """
        df = pd.read_csv(os.path.join(path_to_dir, file_name + ".csv"))
        str_df = "Number of reviews: " + str(df.iloc[:, 0].count())
        return str_df

    def get_pie_chart(path_to_dir: str, file_name: str) -> str:
        """
        Takes path to directory and file name
        Creates a pie chart image with reviews' ratings % distribution
        Returns path to pie chart image
        """
        df = json.load(open(os.path.join(path_to_dir, f"{file_name}.json")))

        cache_path = os.path.join(path_to_dir, f"{file_name}_cache")
        if not (os.path.exists(cache_path)):
            os.mkdir(cache_path)
        path_to_pie_chart = os.path.join(cache_path, "pie_chart.png")
        try:
            os.mkdir(os.path.join(path_to_dir, f"{file_name}_cache"))
        except:
            pass

        amounts = {_: 0 for _ in df["class_names"]}

        for review in df["output_list"]:
            class_name = review["class_name"]
            amounts[class_name] += 1

        # default values
        colors = ["red", "green"]

        if len(df["class_numbers"]) == 3:
            colors = ["red", "#AAAAAA", "green"]
        if len(df["class_numbers"]) == 5:
            colors = ["red", "#FF8888", "#AAAAAA", "#88FF88", "green"]

        fig, ax = plt.subplots()
        ax.pie(
            amounts.values(),
            labels=amounts.keys(),
            autopct="%1.1f%%",
            colors=colors,
        )
        plt.savefig(
            path_to_pie_chart,
            bbox_inches="tight",
        )
        return path_to_pie_chart

    def get_distribution(path_to_dir: str, file_name: str) -> str:

        df = json.load(open(os.path.join(path_to_dir, f"{file_name}.json")))

        cache_path = os.path.join(path_to_dir, f"{file_name}_cache")
        if not (os.path.exists(cache_path)):
            os.mkdir(cache_path)
        path_distribution = os.path.join(cache_path, "distribution.png")

        reviews = df["output_list"]

        confindence_assessments = {
            "[0.5, 0.6)": 0,
            "[0.6, 0.7)": 0,
            "[0.7, 0.8)": 0,
            "[0.8, 0.9)": 0,
            "[0.9, 1]": 0,
        }

        for review in reviews:
            p = review["class_confidence"]
            if 0.5 <= p < 0.6:
                confindence_assessments["[0.5, 0.6)"] += 1
            if 0.6 <= p < 0.7:
                confindence_assessments["[0.6, 0.7)"] += 1
            if 0.7 <= p < 0.8:
                confindence_assessments["[0.7, 0.8)"] += 1
            if 0.8 <= p < 0.9:
                confindence_assessments["[0.8, 0.9)"] += 1
            if 0.9 <= p <= 1.0:
                confindence_assessments["[0.9, 1]"] += 1

        x = list(confindence_assessments.keys())
        y = list(confindence_assessments.values())
        bar_colors = ["#FF0000", "#FF8800", "#FFFF00", "#88FF00", "#00FF00"]

        plt.title("Confidence distibution")
        plt.bar(x, y, color=bar_colors)

        fig, ax = plt.subplots()
        ax.bar(x, y, color=bar_colors)
        plt.savefig(
            path_distribution,
            dpi="figure",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        return path_distribution

    def get_distribution2(path_to_dir: str, file_name: str) -> str:

        df = json.load(open(os.path.join(path_to_dir, f"{file_name}.json")))

        cache_path = os.path.join(path_to_dir, f"{file_name}_cache")
        if not (os.path.exists(cache_path)):
            os.mkdir(cache_path)
        path_distribution2 = os.path.join(cache_path, "distribution2.png")

        reviews = df["output_list"]

        intervals = [
            "[0.5, 0.6)",
            "[0.6, 0.7)",
            "[0.7, 0.8)",
            "[0.8, 0.9)",
            "[0.9, 1]",
        ][::-1]

        confindence_assessments = {_: [0] * len(intervals) for _ in df["class_names"]}

        for review in reviews:
            p = review["class_confidence"]
            i = review["class_name"]
            if 0.5 <= p < 0.6:
                confindence_assessments[i][4] += 1
            if 0.6 <= p < 0.7:
                confindence_assessments[i][3] += 1
            if 0.7 <= p < 0.8:
                confindence_assessments[i][2] += 1
            if 0.8 <= p < 0.9:
                confindence_assessments[i][1] += 1
            if 0.9 <= p <= 1.0:
                confindence_assessments[i][0] += 1

        maximum = 0
        for key in confindence_assessments.keys():
            maximum = max(maximum, max(confindence_assessments[key]))

        confindence_assessments["intervals"] = intervals
        conf_and_ratings = pd.DataFrame(confindence_assessments).set_index("intervals")

        raw_colors = [
            ["#888888", "#FF0000"],
            ["#888888", "#FF8800"],
            ["#888888", "#FFFF00"],
            ["#888888", "#88FF00"],
            ["#888888", "#00FF00"],
        ][::-1]

        CCS = []  # Custom Color Schemes

        for cmap in raw_colors:
            new_cmap = LinearSegmentedColormap.from_list("custom_cmap", cmap)
            CCS.append(new_cmap)

        plt.title("Distribution")
        f, axs = plt.subplots(len(intervals), 1, gridspec_kw={"hspace": 0})

        counter = 0
        for index, row in conf_and_ratings.iterrows():
            sns.heatmap(
                np.array([row.values]),
                yticklabels=[intervals[counter]],
                xticklabels=conf_and_ratings.columns,
                annot=True,
                fmt=".2f",
                ax=axs[counter],
                cmap=CCS[counter],
                cbar=False,
                vmin=0,  # Min scale value
                vmax=maximum,  # Max scale value
            )
            counter += 1

        plt.savefig(
            path_distribution2,
            bbox_inches="tight",
        )
        return path_distribution2

    def get_statistics(path_to_dir: str, file_name: str, more_info=False) -> str:
        df = json.load(open(os.path.join(path_to_dir, f"{file_name}.json")))

        # default values
        amounts = {_: 0 for _ in df["class_names"]}
        labels = df["class_names"]

        for review in df["output_list"]:
            class_name = review["class_name"]
            amounts[class_name] += 1

        amounts = list(amounts.values())

        number_of_reviews = "**Number of reviews:**  \n"

        for i in range(len(df["class_numbers"])):
            number_of_reviews += f"- {labels[i]}: {amounts[i]}  \n"

        number_of_reviews += f"Total: {sum(amounts)}  \n\n"

        if more_info:
            """
            Needs .CSV file with texts of reviews.
            """
            df = pd.read_csv(os.path.join(path_to_dir, f"{file_name}.csv"))
            df = df.rename(columns={"Unnamed: 0": "index", "text": "review"})
            words_number = []
            reviews_lengths = []

            for i in range(len(df["review"])):
                review = df["review"][i]
                words_number.append(len(review.split()))
                reviews_lengths.append(len(review))

            mean_number = round(mean(words_number), 1)
            max_number = max(words_number)
            min_number = min(words_number)
            qu1_number, median_number, qu3_number = quantiles(words_number, n=4)

            mean_length = round(mean(reviews_lengths), 1)
            max_length = max(reviews_lengths)
            min_length = min(reviews_lengths)
            qu1_length, median_length, qu3_length = quantiles(reviews_lengths, n=4)

            table = (
                f"|  | Words Quantity | Symbols Quantity |  \n"
                + "| ---------- | ---------- | --------- |  \n"
                + f"| Minimum | {min_number} | {min_length} |  \n"
                + f"| 1st Qu.| {qu1_number} | {qu1_length} |  \n"
                + f"| Median | {median_number} | {median_length} |  \n"
                + f"| Mean | {mean_number} | {mean_length} |  \n"
                + f"| 3rd Qu. | {qu3_number} | {qu3_length} |  \n"
                + f"| Maximum | {max_number} | {max_length} |  \n"
            )

            number_of_reviews += "**Additional information:**  \n" + table

        return number_of_reviews

    def get_report(path: str, more_info=False) -> None:
        """
        Takes path to file
        Creates summary, pie chart, and statistics
        Saves .MD and .PDF files
        """
        path_to_dir, file_name = os.path.split(path)

        # removes file extention leaving name only
        file_name = ".".join(file_name.split(".")[:-1:])

        path_to_report = os.path.join(path_to_dir, f"{file_name}_report")

        review_summary = Report.get_summary(path_to_dir, file_name)
        review_pie_chart = Report.get_pie_chart(path_to_dir, file_name)
        review_distribution = Report.get_distribution(path_to_dir, file_name)

        report_text = (
            f"# Report on “{file_name}”  \n\n"
            + f"## Summary: {review_summary}  \n\n"
            + f"## Pie chart:  \n![python]({review_pie_chart})  \n\n"
            + f"## Confidence distibution:  \n![python]({review_distribution})  \n\n"
        )

        if more_info:
            review_distribution2 = Report.get_distribution2(path_to_dir, file_name)
            review_stats = Report.get_statistics(
                path_to_dir, file_name, more_info=more_info
            )
            report_text = (
                report_text
                + f"## Statistics:  \n{review_stats}"
                + f"## Confidence distibution by rates:  \n![python]({review_distribution2})  \n\n"
            )

        markdown_file = MdUtils(
            file_name=path_to_report,
        )

        markdown_file.new_paragraph(report_text)

        markdown_file.create_md_file()

        pdf = MarkdownPdf(toc_level=2, optimize=True)
        pdf.add_section(
            Section(
                report_text,
                toc=False,
            ),
            user_css="h1 {text-align:center;}",
        )
        pdf.save(f"{path_to_report}.pdf")


def main():
    path = "/path/to/file.json"
    Report.get_report(path, more_info=True)


if __name__ == "__main__":
    main()

from scraper.nursing import NursingJobs


def main():
    scraper = NursingJobs()
    jobs = scraper.scrape_jobs()

    print(f"Found {len(jobs)} jobs")
    print(jobs.head())

    scraper.save_as_csv(jobs)


if __name__ == "__main__":
    main()

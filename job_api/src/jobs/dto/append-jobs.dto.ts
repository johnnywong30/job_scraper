import { Job } from 'src/jobs/entities/job.entity';

export class AppendJobsDto {
  spreadsheetId: string;
  sheetName: string;
  jobs: Job[];
}

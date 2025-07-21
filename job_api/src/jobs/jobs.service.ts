import { Injectable } from '@nestjs/common';
import { AppendJobsDto } from './dto/append-jobs.dto';
import { GoogleSheetsModule } from 'src/google.sheets/google.sheets.module';

@Injectable()
export class JobsService {
  constructor(private readonly googleSheetsModule: GoogleSheetsModule) {}

  append(appendJobDto: AppendJobsDto) {
    return 'This action appends a jobs to a specific sheet';
  }
}

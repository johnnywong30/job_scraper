import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { JobsService } from './jobs.service';
import { AppendJobsDto } from './dto/append-jobs.dto';

@Controller('jobs')
export class JobsController {
  constructor(private readonly jobsService: JobsService) {}

  @Post()
  append(@Body() appendJobsDto: AppendJobsDto) {
    return this.jobsService.append(appendJobsDto);
  }
}

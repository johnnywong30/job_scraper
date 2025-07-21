import { Module } from '@nestjs/common';
import { JobsService } from './jobs.service';
import { JobsController } from './jobs.controller';
import { GoogleSheetsModule } from 'src/google.sheets/google.sheets.module';

@Module({
  controllers: [JobsController],
  providers: [JobsService],
  imports: [GoogleSheetsModule],
})
export class JobsModule {}

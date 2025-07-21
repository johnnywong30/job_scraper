import { Module } from '@nestjs/common';
import { GoogleSheetsService } from './google.sheets.service';
import { ConfigModule } from '@nestjs/config';

@Module({
  providers: [GoogleSheetsService],
  imports: [ConfigModule],
})
export class GoogleSheetsModule {}

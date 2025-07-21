import {
  Injectable,
  OnModuleInit,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

import { GoogleSheet } from './entities/google.sheet.entity';
import { google, sheets_v4 } from 'googleapis';

@Injectable()
export class GoogleSheetsService implements OnModuleInit {
  constructor(private readonly configService: ConfigService) {}

  private sheets: sheets_v4.Sheets;

  async onModuleInit() {
    const auth = new google.auth.JWT({
      email: this.configService.get<string>('googleApi.clientEmail'),
      key: this.configService.get<string>('googleApi.privateKey'),
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });
    this.sheets = google.sheets({ version: 'v4', auth });
  }

  async checkAccessToSheet(googleSheet: GoogleSheet) {
    try {
      await this.sheets.spreadsheets.get({
        spreadsheetId: googleSheet.id,
        fields: 'spreadsheetId',
      });
      return true;
    } catch (error: any) {
      const status = error?.response?.status;
      if (status === 403 || status === 404 || status === 401) {
        return false;
      }
      throw error;
    }
  }

  async appendToSheet(
    googleSheet: GoogleSheet,
    values: (number | string | Date)[][],
  ) {
    const isAccessible = await this.checkAccessToSheet(googleSheet);
    if (!isAccessible) {
      throw new UnauthorizedException(
        'Service account does not have access to this sheet. Please grant it editor access.',
      );
    }

    const range = `${googleSheet.sheetName}!A1`;
    const response = await this.sheets.spreadsheets.values.append({
      spreadsheetId: googleSheet.id,
      range,
      valueInputOption: 'RAW',
      insertDataOption: 'INSERT_ROWS',
      requestBody: {
        values,
      },
    });

    return response.data;
  }
}

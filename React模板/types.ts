
export interface ChatMessage {
  role: 'user' | 'model';
  text: string;
  isThinking?: boolean;
}

export interface SensorData {
  heartRate: number;
  steps: number;
  stepHistory: number[]; // Added: 7 days of history
  battery: number; // 0-100
  temperature: number;
  weatherIcon: string;
  calories: number;
  humidity: number;
  notifications: number;
  bluetoothConnected: boolean;
  alarmSet: boolean;
  doNotDisturb: boolean;
}

export enum SlotPosition {
  TOP_LEFT = 'TOP_LEFT',
  TOP_MID = 'TOP_MID',
  TOP_RIGHT = 'TOP_RIGHT',
  BTM_LEFT = 'BTM_LEFT',
  BTM_MID = 'BTM_MID',
  BTM_RIGHT = 'BTM_RIGHT',
  MID_L_TOP = 'MID_L_TOP',
  MID_L_BTM = 'MID_L_BTM'
}

export enum WidgetType {
  EMPTY = 'EMPTY',
  DATE = 'DATE',
  BATTERY = 'BATTERY',
  CALORIES = 'CALORIES',
  HEART_RATE = 'HEART_RATE',
  MESSAGES = 'MESSAGES',
  HUMIDITY = 'HUMIDITY',
  WEATHER = 'WEATHER',
  STEPS = 'STEPS',
  STEP_CHART = 'STEP_CHART'
}

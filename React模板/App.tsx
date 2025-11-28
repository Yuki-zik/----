
import React, { useState, useEffect } from 'react';
import { WatchFace } from './components/WatchFace';
import { ChatInterface } from './components/ChatInterface';
import { SettingsMenu } from './components/SettingsMenu';
import { SensorData, WidgetType } from './types';

export default function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Widget State (Lifted from WatchFace)
  // Top Widgets: Expanded to 5 slots [FarL, L, Mid, R, FarR]
  const [topWidgets, setTopWidgets] = useState<WidgetType[]>([
      WidgetType.HUMIDITY, 
      WidgetType.BATTERY, 
      WidgetType.DATE, 
      WidgetType.CALORIES, 
      WidgetType.WEATHER
  ]);
  const [btmWidgets, setBtmWidgets] = useState<WidgetType[]>([WidgetType.HEART_RATE, WidgetType.MESSAGES, WidgetType.HUMIDITY]);
  const [leftWidgets, setLeftWidgets] = useState<WidgetType[]>([WidgetType.WEATHER, WidgetType.STEPS]);

  // Simulated Sensor Data State
  const [sensorData, setSensorData] = useState<SensorData>({
    heartRate: 75,
    steps: 6420,
    stepHistory: [4500, 7200, 3100, 8900, 11200, 5600, 6420], // 7 Days, last is today
    battery: 88,
    temperature: 24,
    weatherIcon: '⛅',
    calories: 1205,
    humidity: 45,
    notifications: 2,
    bluetoothConnected: true,
    alarmSet: true,
    doNotDisturb: false,
  });

  // New State for Sedentary Level (1-5)
  const [sedentaryLevel, setSedentaryLevel] = useState<number>(1);

  // Simulation Effect
  useEffect(() => {
    const interval = setInterval(() => {
      setSensorData(prev => {
        const hrChange = Math.floor(Math.random() * 5) - 2;
        let newHr = prev.heartRate + hrChange;
        
        if (Math.random() > 0.98) newHr = 165; 
        if (newHr > 170) newHr = 140; 
        if (newHr < 40) newHr = 45;

        const stepAdd = Math.floor(Math.random() * 5);
        const batDrain = Math.random() > 0.99 ? 1 : 0;
        
        const newSteps = prev.steps + stepAdd;
        
        // Update history: Last element reflects current steps
        const newHistory = [...prev.stepHistory];
        newHistory[6] = newSteps;

        return {
          ...prev,
          heartRate: newHr,
          steps: newSteps,
          stepHistory: newHistory,
          battery: Math.max(0, prev.battery - batDrain)
        };
      });

      // Simulate Sedentary Level fluctuation
      setSedentaryLevel(prev => {
          if (Math.random() > 0.8) {
              const change = Math.random() > 0.5 ? 1 : -1;
              const next = Math.max(1, Math.min(5, prev + change));
              return next;
          }
          return prev;
      });

    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Handle Widget Updates from Settings Menu
  const handleWidgetUpdate = (section: 'top' | 'btm' | 'left', index: number, type: WidgetType) => {
    if (section === 'top') {
        const newW = [...topWidgets];
        newW[index] = type;
        setTopWidgets(newW);
    } else if (section === 'btm') {
        const newW = [...btmWidgets];
        newW[index] = type;
        setBtmWidgets(newW);
    } else {
        const newW = [...leftWidgets];
        newW[index] = type;
        setLeftWidgets(newW);
    }
  };

  // Handle Widget Cycle (Click on Watch Face)
  const handleWidgetCycle = (section: 'top' | 'btm' | 'left', index: number) => {
      const allTypes = Object.values(WidgetType).filter(t => t !== WidgetType.EMPTY);
      
      let currentList: WidgetType[];
      if (section === 'top') currentList = topWidgets;
      else if (section === 'btm') currentList = btmWidgets;
      else currentList = leftWidgets;

      const currentType = currentList[index];
      const typeIndex = allTypes.indexOf(currentType);
      const nextType = allTypes[(typeIndex + 1) % allTypes.length];
      
      handleWidgetUpdate(section, index, nextType);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] flex flex-col items-center justify-center relative overflow-hidden text-slate-300 selection:bg-cyan-500/30">
        
      {/* Background Ambience */}
      <div className="absolute inset-0 grid grid-cols-[repeat(20,minmax(0,1fr))] grid-rows-[repeat(20,minmax(0,1fr))] opacity-[0.03] pointer-events-none">
          {Array.from({ length: 400 }).map((_, i) => (
              <div key={i} className="border border-slate-500/20" />
          ))}
      </div>
      
      {/* Header / Brand */}
      <div className="absolute top-8 left-8 z-40 pointer-events-none">
          <h1 className="text-2xl font-bold tracking-[0.2em] text-slate-500 font-[Rajdhani]">PROJECT <span className="text-cyan-500">SYNAPSE</span></h1>
          <p className="text-xs text-slate-600 font-mono mt-1">TACTICAL TERMINAL PROTOTYPE v7.0</p>
      </div>

      {/* External Settings Button */}
      <div className="absolute top-8 right-8 z-40">
        <button 
          onClick={() => setIsSettingsOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-700 hover:border-cyan-500 text-slate-300 hover:text-cyan-400 rounded-sm transition-all font-mono text-xs tracking-widest uppercase group active:scale-95 shadow-lg shadow-black/50"
        >
          <span className="material-icons text-sm group-hover:rotate-90 transition-transform">settings</span>
          表盘配置
        </button>
      </div>

      {/* Main Watch Container */}
      <div className={`relative z-10 flex flex-col items-center gap-12 scale-125 md:scale-150 transform transition-transform duration-500 ${isSettingsOpen ? 'translate-x-12' : ''}`}>
        <div className="relative">
             <WatchFace 
                sensorData={sensorData} 
                sedentaryLevel={sedentaryLevel}
                onOpenChat={() => setIsChatOpen(true)}
                onOpenSettings={() => setIsSettingsOpen(true)}
                widgetConfig={{ topWidgets, btmWidgets, leftWidgets }}
                onWidgetCycle={handleWidgetCycle}
            />
        </div>
        
        {/* Instructions */}
        <div className="text-center opacity-50 text-[10px] font-mono tracking-widest max-w-xs transition-opacity duration-300" style={{ opacity: isSettingsOpen ? 0 : 0.5 }}>
            <p className="mb-2">/// INTERACTION LOG ///</p>
            <p>CLICK WIDGETS TO CYCLE DATA</p>
        </div>
      </div>

      {/* Overlays */}
      <SettingsMenu 
        isOpen={isSettingsOpen} 
        onClose={() => setIsSettingsOpen(false)} 
        config={{ topWidgets, btmWidgets, leftWidgets }}
        onUpdate={handleWidgetUpdate}
      />
      
      <ChatInterface isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

      {/* Footer Info */}
      <div className="absolute bottom-4 right-4 text-right z-40 pointer-events-none">
          <div className="flex items-center justify-end gap-2 text-xs text-slate-600 font-mono">
             <span>GEN 3 PRO INTELLIGENCE</span>
             <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          </div>
      </div>
    </div>
  );
}

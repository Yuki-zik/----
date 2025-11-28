using Toybox.ActivityMonitor as AM;
using Toybox.Graphics as G;
using Toybox.Lang as Lang;
using Toybox.Math as Math;
using Toybox.System as Sys;
using Toybox.Time as Time;
using Toybox.WatchUi as Ui;

const COLOR_CYAN   = 0x06b6d4;
const COLOR_SLATE  = 0x64748b;
const COLOR_MUTED  = 0x334155;
const COLOR_RED    = 0xef4444;
const COLOR_GREEN  = 0x22c55e;
const COLOR_WHITE  = G.COLOR_WHITE;
const COLOR_BG     = G.COLOR_BLACK;
const STEP_GOAL    = 10000;
const MOCK_MODE    = true; // 开启模拟数据，方便无传感器时排版

class WidgetSlot {
    var label;
    var getter;
    var pos;       // [x, y]
    var fontLabel;
    var fontValue;
    var color;

    function initialize(label, getter, pos, fontLabel, fontValue, color) {
        self.label = label;
        self.getter = getter;
        self.pos = pos;
        self.fontLabel = fontLabel;
        self.fontValue = fontValue;
        self.color = color;
    }

    function draw(dc) {
        var val = getter != null ? getter.invoke() : "";
        dc.setColor(COLOR_SLATE, COLOR_BG);
        dc.drawText(pos[0], pos[1] - 10, fontLabel, label, G.TEXT_JUSTIFY_CENTER);
        dc.setColor(color, COLOR_BG);
        dc.drawText(pos[0], pos[1] + 6, fontValue, val, G.TEXT_JUSTIFY_CENTER);
    }
}

class SynapseView extends Ui.WatchFace {
    var _center;
    var _topSlots;
    var _bottomSlots;
    var _leftSlots;
    var _fontTimeLarge;
    var _fontTimeSmall;
    var _fontLabel;
    var _fontValue;

    function initialize() {
        Ui.WatchFace.initialize();
        _topSlots = [];
        _bottomSlots = [];
        _leftSlots = [];
    }

    function onLayout(dc) {
        _center = [dc.getWidth() / 2, dc.getHeight() / 2];
        _topSlots = [];
        _bottomSlots = [];
        _leftSlots = [];

        _fontTimeLarge = G.FONT_LARGE;    // safe system font for big hours
        _fontTimeSmall = G.FONT_MEDIUM;   // minutes
        _fontLabel = G.FONT_XTINY;
        _fontValue = G.FONT_TINY;

        var radius = 118;
        var topAngles = [-150, -110, -70, -30]; // spread wider to edge
        var topLabels = ["BATT", "HUM", "WEA", "DATE"];
        var topGetters = [
            method(:_getBattery),
            method(:_getHumidity),
            method(:_getWeather),
            method(:_getDateShort)
        ];
        for (var i = 0; i < topAngles.size(); i++) {
            var p = _polar(radius, topAngles[i]);
            _topSlots.add(new WidgetSlot(topLabels[i], topGetters[i], p, _fontLabel, _fontValue, COLOR_CYAN));
        }

        var bottomAngles = [210, 270, 330];
        var bottomLabels = ["HR", "MSG", "STEPS"];
        var bottomGetters = [
            method(:_getHeartRate),
            method(:_getNotifications),
            method(:_getStepsShort)
        ];
        var bottomColors = [COLOR_RED, COLOR_GREEN, COLOR_CYAN];
        for (var j = 0; j < bottomAngles.size(); j++) {
            var pb = _polar(radius - 4, bottomAngles[j]);
            _bottomSlots.add(new WidgetSlot(bottomLabels[j], bottomGetters[j], pb, _fontLabel, _fontValue, bottomColors[j]));
        }

        var leftX = _center[0] - 90;
        _leftSlots.add(new WidgetSlot("ENV.DATA", method(:_getWeather), [leftX, _center[1] - 18], _fontLabel, _fontValue, COLOR_RED));
        _leftSlots.add(new WidgetSlot("PEDO", method(:_getSteps), [leftX, _center[1] + 18], _fontLabel, _fontValue, COLOR_RED));
    }

    function onUpdate(dc) {
        var amInfo = AM.getInfo();

        dc.setColor(G.COLOR_BLACK, G.COLOR_BLACK);
        dc.clear();

        _drawGrid(dc);
        _drawDecor(dc);
        _drawDayArc(dc);
        _drawStepArc(dc, amInfo);
        _drawTopBar(dc);
        _drawBottomBar(dc, amInfo);

        for (var i = 0; i < _topSlots.size(); i++) {
            _topSlots[i].draw(dc);
        }
        for (var j = 0; j < _bottomSlots.size(); j++) {
            _bottomSlots[j].draw(dc);
        }
        for (var k = 0; k < _leftSlots.size(); k++) {
            _leftSlots[k].draw(dc);
        }

        _drawCenterTime(dc);
        _drawFooter(dc);
    }

    // --- Data getters ---
    function _getHeartRate() {
        var info = AM.getInfo();
        if (info != null && (info has :currentHeartRate) && info.currentHeartRate != null) {
            return Lang.format("%d bpm", [info.currentHeartRate]);
        }
        if (MOCK_MODE) {
            return "164 bpm";
        }
        return "-- bpm";
    }

    function _getSteps() {
        var info = AM.getInfo();
        if (info != null && info.steps != null) {
            return Lang.format("%d", [info.steps]);
        }
        if (MOCK_MODE) {
            return "7156";
        }
        return "--";
    }

    function _getStepsShort() {
        var info = AM.getInfo();
        if (info != null && info.steps != null) {
            var pct = (info.steps * 100.0) / STEP_GOAL;
            if (pct > 100) {
                pct = 100;
            }
            return Lang.format("%d%%", [Math.round(pct)]);
        }
        if (MOCK_MODE) {
            return "72%";
        }
        return "--";
    }

    function _getBattery() {
        var stats = Sys.getSystemStats();
        return Lang.format("%d%%", [stats.battery]);
    }

    function _getBatteryPct() {
        var stats = Sys.getSystemStats();
        if (stats != null && stats.battery != null) {
            return stats.battery;
        }
        return MOCK_MODE ? 87 : 0;
    }

    function _getDateShort() {
        var info = Time.Gregorian.info(Time.now(), Time.FORMAT_SHORT);
        return Lang.format("%02d/%02d", [info.day, info.month]);
    }

    function _getCalories() {
        var info = AM.getInfo();
        if (info != null && info.calories != null) {
            return Lang.format("%d kcal", [info.calories]);
        }
        return "kcal --";
    }

    function _getHumidity() {
        if (MOCK_MODE) {
            return "45%";
        }
        return "45%";
    }

    function _getHumidityPct() {
        if (MOCK_MODE) {
            return 45;
        }
        return 45;
    }

    function _getWeather() {
        if (MOCK_MODE) {
            return "24°C";
        }
        return "22°C";
    }

    function _getNotifications() {
        return "MSG";
    }

    // --- Drawing helpers ---
    function _polar(radius, deg) {
        var rad = deg * Math.PI / 180.0;
        return [
            _center[0] + Math.round(radius * Math.cos(rad)),
            _center[1] + Math.round(radius * Math.sin(rad))
        ];
    }

    function _drawGrid(dc) {
        dc.setColor(COLOR_MUTED, COLOR_BG);
        var spacing = 34;
        var w = dc.getWidth();
        var h = dc.getHeight();
        for (var x = 0; x <= w; x += spacing) {
            dc.drawLine(x, 0, x, h);
        }
        for (var y = 0; y <= h; y += spacing) {
            dc.drawLine(0, y, w, y);
        }
        dc.setColor(COLOR_MUTED, COLOR_BG);
        dc.drawCircle(_center[0], _center[1], 128);
    }

    function _drawDecor(dc) {
        // minimal decor: inner circle
        dc.setColor(COLOR_MUTED, COLOR_BG);
        dc.drawCircle(_center[0], _center[1], 70);
    }

    function _drawArcSegment(dc, radius, startDeg, sweepDeg, progress, colorActive, colorDim) {
        var size = radius * 2;
        dc.setColor(colorDim, COLOR_BG);
        dc.drawArc(_center[0] - radius, _center[1] - radius, size, size, startDeg, sweepDeg);
        var activeSweep = sweepDeg * progress;
        if (activeSweep > 0) {
            dc.setColor(colorActive, COLOR_BG);
            dc.drawArc(_center[0] - radius, _center[1] - radius, size, size, startDeg, activeSweep);
        }
    }

    function _drawDayArc(dc) {
        var info = Time.Gregorian.info(Time.now(), Time.FORMAT_SHORT);
        var minutes = info.hour * 60 + info.min;
        var progress = minutes / 1440.0;
        _drawArcSegment(dc, 115, -150, 120, progress, COLOR_CYAN, COLOR_MUTED);
    }

    function _drawStepArc(dc, amInfo) {
        var steps = (amInfo != null && amInfo.steps != null) ? amInfo.steps : 0;
        var progress = steps / STEP_GOAL;
        if (progress > 1) {
            progress = 1;
        }
        _drawArcSegment(dc, 123, 200, 140, progress, COLOR_CYAN, COLOR_MUTED);
    }

    // Top horizontal stats bar (battery / humidity / temp)
    function _drawTopBar(dc) {
        var w = dc.getWidth();
        var barY = 28;
        var barH = 6;
        var pad = 24;
        var barW = w - pad * 2;

        // Battery bar (left third)
        var battPct = _getBatteryPct();
        var segW = barW / 3;
        var bx = pad;
        dc.setColor(COLOR_MUTED, COLOR_BG);
        dc.drawRectangle(bx, barY, segW, barH);
        dc.setColor(COLOR_CYAN, COLOR_BG);
        dc.fillRectangle(bx, barY, (segW * battPct) / 100, barH);
        dc.drawText(bx + segW / 2, barY - 10, _fontLabel, Lang.format("%d%%", [battPct]), G.TEXT_JUSTIFY_CENTER);

        // Humidity bar (middle)
        var humPct = _getHumidityPct();
        var hx = pad + segW + 6;
        dc.setColor(COLOR_MUTED, COLOR_BG);
        dc.drawRectangle(hx, barY, segW, barH);
        dc.setColor(COLOR_CYAN, COLOR_BG);
        dc.fillRectangle(hx, barY, (segW * humPct) / 100, barH);
        dc.drawText(hx + segW / 2, barY - 10, _fontLabel, Lang.format("%d%%", [humPct]), G.TEXT_JUSTIFY_CENTER);

        // Temp label (right)
        var tx = pad + (segW * 2) + 12;
        dc.setColor(COLOR_SLATE, COLOR_BG);
        dc.drawRectangle(tx, barY, segW - 6, barH);
        dc.setColor(COLOR_RED, COLOR_BG);
        dc.drawText(tx + (segW - 6) / 2, barY - 10, _fontLabel, _getWeather(), G.TEXT_JUSTIFY_CENTER);
    }

    // Bottom horizontal step goal bar
    function _drawBottomBar(dc, amInfo) {
        var w = dc.getWidth();
        var barY = dc.getHeight() - 30;
        var barH = 8;
        var pad = 24;
        var barW = w - pad * 2;
        var steps = (amInfo != null && amInfo.steps != null) ? amInfo.steps : (MOCK_MODE ? 7156 : 0);
        var pct = (steps * 1.0) / STEP_GOAL;
        if (pct > 1) {
            pct = 1;
        }
        dc.setColor(COLOR_MUTED, COLOR_BG);
        dc.drawRectangle(pad, barY, barW, barH);
        dc.setColor(COLOR_GREEN, COLOR_BG);
        dc.fillRectangle(pad, barY, barW * pct, barH);
        dc.drawText(_center[0], barY - 10, _fontLabel, Lang.format("%d / 10K", [steps]), G.TEXT_JUSTIFY_CENTER);
    }

    function _drawCenterTime(dc) {
        var info = Time.Gregorian.info(Time.now(), Time.FORMAT_SHORT);
        var hStr = Lang.format("%02d", [info.hour]);
        var mStr = Lang.format("%02d", [info.min]);

        dc.setColor(COLOR_RED, COLOR_BG);
        dc.drawText(_center[0] + 30, _center[1] - 20, _fontTimeLarge, hStr, G.TEXT_JUSTIFY_CENTER);
        dc.setColor(COLOR_WHITE, COLOR_BG);
        dc.drawText(_center[0] - 10, _center[1] + 26, _fontTimeSmall, mStr, G.TEXT_JUSTIFY_CENTER);
    }

    function _drawFooter(dc) {
        dc.setColor(COLOR_SLATE, COLOR_BG);
        dc.drawText(_center[0], dc.getHeight() - 14, _fontLabel, "GOAL 10K", G.TEXT_JUSTIFY_CENTER);
    }

    function _monthAbbrev(m) {
        return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][m - 1];
    }
}

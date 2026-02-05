/**
 * Common chart configuration and styles
 * Used across all chart components for consistent styling
 */

// Color palette
export const CHART_COLORS = {
  primary: '#366164',
  secondary: '#9FB69F',
  text: '#2C3E38',
  textSecondary: '#6B7280',
  border: '#D1D5DB',
  borderLight: '#E5E7EB',
  background: 'rgba(255, 255, 255, 0.95)',
  tooltip: '#6a7985',
  compass: '#2FA4A9'
};

// Font family
export const FONT_FAMILY = 'Raleway, sans-serif';

// Common text styles
export const TEXT_STYLES = {
  title: {
    fontFamily: FONT_FAMILY,
    fontSize: 18,
    fontWeight: 600,
    color: CHART_COLORS.text
  },
  legend: {
    fontFamily: FONT_FAMILY,
    fontSize: 13,
    color: CHART_COLORS.text
  },
  legendSmall: {
    fontFamily: FONT_FAMILY,
    fontSize: 12,
    color: CHART_COLORS.text
  },
  axis: {
    fontFamily: FONT_FAMILY,
    color: CHART_COLORS.textSecondary
  },
  tooltip: {
    color: CHART_COLORS.text,
    fontFamily: FONT_FAMILY
  }
};

// Common timeline configuration
export const TIMELINE_CONFIG = {
  axisType: 'category',
  autoPlay: false,
  playInterval: 2000,
  left: 'center',
  bottom: 0,
  width: '70%',
  label: {
    formatter: '{value}',
    color: CHART_COLORS.text,
    fontFamily: FONT_FAMILY
  },
  lineStyle: {
    color: CHART_COLORS.secondary
  },
  itemStyle: {
    color: CHART_COLORS.secondary,
    borderColor: CHART_COLORS.secondary
  },
  checkpointStyle: {
    color: CHART_COLORS.primary,
    borderColor: CHART_COLORS.primary
  },
  controlStyle: {
    color: CHART_COLORS.secondary,
    borderColor: CHART_COLORS.secondary
  }
};

// Common title configuration
export const getTitleConfig = (text) => ({
  text,
  left: 'center',
  top: 20,
  textStyle: TEXT_STYLES.title
});

// Common tooltip configuration
export const TOOLTIP_CONFIG = {
  backgroundColor: CHART_COLORS.background,
  borderColor: CHART_COLORS.borderLight,
  borderWidth: 1,
  textStyle: TEXT_STYLES.tooltip
};

// Grid configuration for standard charts
export const GRID_CONFIG = {
  left: '3%',
  right: '4%',
  bottom: '3%',
  top: 100,
  containLabel: true
};

// Axis line style
export const AXIS_LINE_STYLE = {
  lineStyle: {
    color: CHART_COLORS.border
  }
};

// Split line style
export const SPLIT_LINE_STYLE = {
  lineStyle: {
    color: CHART_COLORS.borderLight,
    type: 'dashed'
  }
};

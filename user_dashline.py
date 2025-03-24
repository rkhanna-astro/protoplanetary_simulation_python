import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def user_dashline(xdata, ydata, dash1, gap1, dash2, gap2, NaNreg=None, **kwargs):
    """
    Function to produce accurate dotted and dashed lines in Python
    
    Parameters:
    xdata, ydata - Input data coordinates
    dash1, gap1 - Lengths of first dash and gap (mm)
    dash2, gap2 - Lengths of second dash and gap (mm)
    NaNreg - Regions to exclude (list of tuples [(start1, end1, start2, end2), ...])
    **kwargs - Line properties passed to matplotlib
    
    Returns:
    h1, h2 - Handles to the plotted lines and markers
    """
    
    # Convert inputs to numpy arrays and ensure proper shape
    xdata = np.asarray(xdata).ravel()
    ydata = np.asarray(ydata).ravel()
    
    if len(xdata) != len(ydata):
        raise ValueError('xdata and ydata must have the same length')
    
    # Check dash/gap parameters
    if not isinstance(gap1, (int, float)) or gap1 < 0 or not isinstance(gap2, (int, float)) or gap2 < 0:
        raise ValueError('Gaps must be positive numbers')
    
    # Handle case with no gaps
    if gap1 == 0 and gap2 == 0:
        line = plt.plot(xdata, ydata, **kwargs)
        return line[0], None
    
    # Handle marker specifications
    Marker1 = None
    Marker2 = None
    
    if isinstance(dash1, str):
        Marker1 = dash1
        dash1 = 0
    elif dash1 == 0:
        Marker1 = '.'
    
    if isinstance(dash2, str):
        Marker2 = dash2
        dash2 = 0
    elif dash2 == 0:
        Marker2 = '.'
    
    # Get current axis properties
    ax = plt.gca()
    fig = plt.gcf()
    
    # Convert figure size to mm
    fig_width_mm = fig.get_size_inches()[0] * 25.4
    fig_height_mm = fig.get_size_inches()[1] * 25.4
    
    # Get axis limits and scale
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    is_xlog = ax.get_xscale() == 'log'
    is_ylog = ax.get_yscale() == 'log'
    
    # Calculate data positions in mm
    if is_xlog:
        xpos_mm = (np.log10(xdata) - np.log10(xlim[0])) / (np.log10(xlim[1]) - np.log10(xlim[0])) * fig_width_mm
    else:
        xpos_mm = (xdata - xlim[0]) / (xlim[1] - xlim[0]) * fig_width_mm
    
    if is_ylog:
        ypos_mm = (np.log10(ydata) - np.log10(ylim[0])) / (np.log10(ylim[1]) - np.log10(ylim[0])) * fig_height_mm
    else:
        ypos_mm = (ydata - ylim[0]) / (ylim[1] - ylim[0]) * fig_height_mm
    
    # Calculate cumulative distance along line
    dx = np.diff(xpos_mm)
    dy = np.diff(ypos_mm)
    dist = np.insert(np.cumsum(np.sqrt(dx**2 + dy**2)), 0, 0)
    
    # Generate dash pattern
    pattern_length = dash1 + gap1 + dash2 + gap2
    starts = np.arange(0, dist[-1], pattern_length)
    
    # Create dash segments
    dash_segments = []
    for start in starts:
        # First dash
        if dash1 > 0:
            dash_segments.append((start, start + dash1))
        # First gap
        dash_segments.append((start + dash1, start + dash1 + gap1))
        # Second dash
        if dash2 > 0:
            dash_segments.append((start + dash1 + gap1, start + dash1 + gap1 + dash2))
        # Second gap
        dash_segments.append((start + dash1 + gap1 + dash2, start + pattern_length))
    
    # Interpolate data points for each dash segment
    x_dashes = []
    y_dashes = []
    markers1 = []
    markers2 = []
    
    for seg_start, seg_end in dash_segments:
        # Find points within this segment
        mask = (dist >= seg_start) & (dist <= seg_end)
        if not np.any(mask):
            continue
            
        # Interpolate segment endpoints
        if is_xlog:
            x_seg = 10**np.interp([seg_start, seg_end], dist[mask], np.log10(xdata[mask]))
        else:
            x_seg = np.interp([seg_start, seg_end], dist[mask], xdata[mask])
            
        if is_ylog:
            y_seg = 10**np.interp([seg_start, seg_end], dist[mask], np.log10(ydata[mask]))
        else:
            y_seg = np.interp([seg_start, seg_end], dist[mask], ydata[mask])
        
        # Add to dashes or markers
        if seg_end - seg_start == dash1 and Marker1:
            markers1.append((x_seg[0], y_seg[0]))
        elif seg_end - seg_start == dash2 and Marker2:
            markers2.append((x_seg[0], y_seg[0]))
        else:
            x_dashes.extend(x_seg)
            y_dashes.extend(y_seg)
            x_dashes.append(np.nan)
            y_dashes.append(np.nan)
    
    # Apply NaN regions if specified
    if NaNreg is not None:
        for region in NaNreg:
            if len(region) != 4:
                continue
            mask = ((x_dashes > region[0]) & (x_dashes < region[1])) | \
                   ((x_dashes > region[2]) & (x_dashes < region[3]))
            x_dashes = np.array(x_dashes)
            y_dashes = np.array(y_dashes)
            x_dashes[mask] = np.nan
            y_dashes[mask] = np.nan
    
    # Create plot objects
    h1 = None
    h2 = None
    
    if len(x_dashes) > 0:
        h1 = plt.plot(x_dashes, y_dashes, **kwargs)[0]
    
    if markers1:
        x_m1, y_m1 = zip(*markers1)
        h2 = plt.plot(x_m1, y_m1, linestyle='None', marker=Marker1, **kwargs)[0]
    
    if markers2 and not markers1:
        x_m2, y_m2 = zip(*markers2)
        h2 = plt.plot(x_m2, y_m2, linestyle='None', marker=Marker2, **kwargs)[0]
    elif markers2:
        x_m2, y_m2 = zip(*markers2)
        plt.plot(x_m2, y_m2, linestyle='None', marker=Marker2, **kwargs)
    
    return h1, h2

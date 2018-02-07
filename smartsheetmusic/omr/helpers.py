import numpy as np
from PIL import Image

def get_staff_lines(image):

    sheet = np.asarray(image.convert('L')).astype('float32')/255
    
    # Find Staff Lines
    scan_line = 1-np.mean(sheet, axis=1)
    scan_peak_thresh = np.mean(scan_line) + 2.5*np.std(scan_line)
    scan_filtered = scan_line>scan_peak_thresh
    
    scan_peak_locs = np.where(scan_filtered)[0]
    whitespace_widths = np.append(scan_peak_locs,1)-np.append(0, scan_peak_locs)
    whitespace_widths = whitespace_widths[:-1]
    
    
    staff = []
    for i in range(len(whitespace_widths)):
        if whitespace_widths[i]>4:
            staff.append({'position': scan_peak_locs[i], 'start': scan_peak_locs[i], 'end': scan_peak_locs[i], 'bars': []})
        else:
            staff[-1]['end'] = scan_peak_locs[i]
            staff[-1]['position'] = (staff[-1]['start']+staff[-1]['end'])/2
    
    for n in range(0, len(staff), 10):
        idx = slice(staff[n]['start'],staff[n+9]['start'])
        patch = sheet[idx, :]<0.5
        line = np.mean(patch, axis=0)
        peak_thresh = line.max()*0.9
        peak_locs = np.where(line>peak_thresh)[0]
        
        whitespace_widths = np.append(peak_locs,1)-np.append(0, peak_locs)
        whitespace_widths = whitespace_widths[:-1]        
        
        bars = []
        for i in range(len(whitespace_widths)):
            if whitespace_widths[i]>4:
                bars.append(peak_locs[i])
            else:
                bars[-1] = (bars[-1]+peak_locs[i])/2
                
        for i in range(5):
            staff[n+i]['bars'] = bars
            
    return staff


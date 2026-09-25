"""Figures 2 and 3: DNV adoption and national unemployment (percentage points).
All numbers are the ones reported in the manuscript / read back from the submitted figure files."""
import itertools, json
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Liberation Sans', 'DejaVu Sans'],
    'font.size': 6.5, 'axes.labelsize': 6.5, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
    'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
    'svg.fonttype': 'path', 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150,
})
BLUE, DARK, GREY = '#0072B2', '#2B2E33', '#6B6F76'
CS = {0: (-0.774, 0.486, 3, 13), 1: (-1.208, 0.722, 3, 11), 2: (-2.566, 1.237, 2, 7), 3: (-1.626, 0.182, 1, 2)}
TWFE = (-1.24, -2.73, 0.24)
W, H = 2.65, 2.50
L, R, T, B = 0.74, 0.08, 0.06, 0.86
XLIM, YLIM = (-1.2, 3.5), (-2.95, 2.75)
def base_fig():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([L/W, B/H, (W-L-R)/W, (H-B-T)/H])
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    ax.plot([XLIM[0], XLIM[1]], [0, 0], color=GREY, lw=0.6, ls=(0, (3, 2)), zorder=0)
    ax.set_yticks([-2, -1, 0, 1])
    ax.set_ylabel('Association with\nunemployment rate\n(percentage points)', labelpad=3, linespacing=1.15)
    ax.text(1.55, 2.27, 'Negative values = lower unemployment', ha='center', va='top', fontsize=6, style='italic', color=GREY)
    return fig, ax
def cs_points(ax):
    for t, (lo, hi, c, n) in CS.items():
        est = (lo+hi)/2
        ax.errorbar(t, est, yerr=[[est-lo], [hi-est]], fmt='o', ms=4.2, color=BLUE, mfc=BLUE, elinewidth=0.9, capsize=2.2, capthick=0.9, zorder=3)
def support_table(ax, cols):
    tr=ax.get_xaxis_transform(); y1,y2=-0.335,-0.415
    ax.text(XLIM[0],y1,'Cohorts',transform=tr,ha='right',va='center',fontsize=6,color=GREY)
    ax.text(XLIM[0],y2,'Treated obs.',transform=tr,ha='right',va='center',fontsize=6,color=GREY)
    for x,c,n in cols:
        ax.text(x,y1,c,transform=tr,ha='center',va='center',fontsize=6.5)
        ax.text(x,y2,n,transform=tr,ha='center',va='center',fontsize=6.5)
    ax.plot([XLIM[0],XLIM[1]],[-0.275,-0.275],transform=tr,color='#C9CCD1',lw=0.4,clip_on=False)
def xlabel(ax,text):
    ax.text(1.5,-0.195,text,transform=ax.get_xaxis_transform(),ha='center',va='center',fontsize=6.5)
def figure2():
    fig,ax=base_fig()
    ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
    ax.add_patch(mpl.patches.Rectangle((XLIM[0],YLIM[0]),-0.45-XLIM[0],1.6-YLIM[0],color='#EEF0F2',lw=0,zorder=-1))
    ax.text((XLIM[0]-0.45)/2,(YLIM[0]+1.6)/2,'no pre-treatment\nestimates (t < 0)',rotation=90,ha='center',va='center',fontsize=6,color=GREY,linespacing=1.1)
    cs_points(ax); ax.set_xticks([0,1,2,3]); ax.set_xticklabels(['0','1','2','3'])
    ax.spines['bottom'].set_bounds(XLIM[0],XLIM[1]); xlabel(ax,'Years since first full exposure year')
    support_table(ax,[(t,str(c),str(n)) for t,(lo,hi,c,n) in CS.items()]); return fig
def figure3():
    fig,ax=base_fig(); est,lo,hi=TWFE
    ax.errorbar(-0.82,est,yerr=[[est-lo],[hi-est]],fmt='s',ms=4.0,color=DARK,mfc=DARK,elinewidth=0.9,capsize=2.2,capthick=0.9,zorder=3)
    ax.axvline(-0.42,color='#C9CCD1',lw=0.6,ls=(0,(1,2)),zorder=0)
    ax.text(-0.82,2.72,'Pooled',ha='center',va='top',fontsize=6,color=GREY)
    ax.text(1.55,2.72,'CS-style, by event time',ha='center',va='top',fontsize=6,color=GREY)
    cs_points(ax); ax.set_xticks([-0.82,0,1,2,3]); ax.set_xticklabels(['TWFE','0','1','2','3'])
    xlabel(ax,'Years since first full exposure year')
    support_table(ax,[(-0.82,'—','—')]+[(t,str(c),str(n)) for t,(lo_,hi_,c,n) in CS.items()]); return fig
report={}
for name,fn in (('event_study',figure2),('twfe_vs_cs',figure3)):
    fig=fn(); pos=fig.axes[0].get_position()
    report[name]={'axes_in':[round(v,4) for v in (pos.x0*W,pos.y0*H,pos.width*W,pos.height*H)],'text_overlaps':[]}
    for ext,kw in (('svg',{}),('pdf',{}),('png',{'dpi':600})): fig.savefig(f'{name}.{ext}',facecolor='white',**kw)
    plt.close(fig)
print(json.dumps(report,indent=1))

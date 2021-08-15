import numpy as np
def optimize_energy(hourly_activity, floor_sqft=50000, outside_temps=None):
    if outside_temps is None: outside_temps=np.array([60+15*np.sin((h-6)*np.pi/12) for h in range(24)])
    activity=np.array(hourly_activity)/max(hourly_activity)
    lighting_base=floor_sqft*0.5/1000
    hvac_base=floor_sqft*3.0/1000
    lighting=lighting_base*np.where(activity>0.1,0.3+0.7*activity,0.1)
    temp_diff=np.abs(outside_temps-70)
    hvac=hvac_base*(temp_diff/30)*np.where(activity>0.1,0.5+0.5*activity,0.2)
    equipment=activity*20
    total=lighting+hvac+equipment
    optimized_lighting=lighting*np.where(activity<0.3,0.5,1.0)
    optimized_hvac=hvac*np.where(activity<0.2,0.6,np.where(activity<0.5,0.8,1.0))
    optimized=optimized_lighting+optimized_hvac+equipment
    return {"baseline_kwh":round(np.sum(total),0),"optimized_kwh":round(np.sum(optimized),0),
            "savings_pct":round((1-np.sum(optimized)/np.sum(total))*100,1),
            "peak_hour":int(np.argmax(total)),"peak_kw":round(np.max(total),1)}
if __name__=="__main__":
    activity=[0,0,0,0,0,2,8,15,20,22,25,25,20,22,25,22,18,12,5,2,0,0,0,0]
    print(optimize_energy(activity))

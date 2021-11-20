<template>
<div>
     <table  height="12%"  width="100%">
 



<tr>
<td  width="12%"  style="background-color:#bfbfbf">
<IM  height=50 src="logo.gif" width=100></IM></td>
<td  width="88%" style="background-color:#bfbfbf">
<MARQUEE scrollDelay=1 behavior=slide>
<h3 style="color:#000040"> MTP Web Site...</h3>
<h4 style="color:#800000">Designed for Enterprise level Information Sharing</h4>
</MARQUEE>
</td>
</tr>
</table>
    <table Style="position: absolute;  height: 100%; width: 100%;"  BACKGROUND="t4.gif">
        <tr valign="top" >
            <td width="1%" ></td>
            <td width="34%" >
                <ul style="list-style-type:none;padding-left:30px;"> 
                    <li style="padding-top:10px;"> <a :href="api_root+'/design'" target="_blank">Products catalogue</a></li>
                    <li style="padding-top:10px;"> <router-link to="/balancehom">HOM Balance</router-link></li>
                   
                    <li style="padding-top:10px;"> <router-link to="/balancebom">BOM Balance</router-link></li>
                    <li style="padding-top:10px;"> <router-link to="/searchdatabase">Search design database</router-link></li>
                    <li style="padding-top:10px;"> <router-link to="/dailymislipitems">Daily MI slip Items</router-link></li>
                    <li style="padding-top:10px;"> <router-link to="/oplayout">Operation layout</router-link></li>
                    <li style="padding-top:10px;"> <router-link to="/prodprogram" target="_blank">Production Program</router-link></li>
                    <li style="padding-top:10px;"> <a :href="api_root+'/mtpinfoshare/pendingmislips'" target="_blank">Pending MI Slips</a></li>
                    
                    <li style="padding-top:10px;"><router-link to="/manpowerutilization" target="_blank">Manpower Utilization</router-link></li>
                    <li style="padding-top:10px;"><router-link to="/machineutilization" target="_blank">Machine Utilization</router-link></li>
                    <li style="padding-top:10px;"><a :href="api_root+'/hr'" target="_blank">HR Data</a></li>

                    <li style="padding-top:10px;"><a :href="api_root+'/mtpinfoshare/ratestockno'" target="_blank">Find rate</a></li>
                    <li style="padding-top:10px;"><a :href="api_root+'/ppc'" target="_blank">Small parts monitoring app</a></li>
                    <li style="padding-top:10px;"><a :href="api_root+'/mi'" target="_blank">Incoming materials app</a></li>
                    <li style="padding-top:10px;"><router-link to="/homiteminfo" target="_blank">HOM Item Status</router-link></li>
                    <li style="padding-top:10px;"><router-link to="/stocknodetail" target="_blank">BOM Item Status</router-link></li>
                    <li style="padding-top:10px;"><router-link to="/dailymrr" target="_blank">Daily MRRs</router-link></li>
                    <li style="padding-top:10px;"><router-link to="/cncpackages" target="_blank">CNC Packages</router-link></li>
                    <li style="padding-top:10px;"><router-link to="/finddrwgno" target="_blank">Find drawing No</router-link></li>
                </ul>
            </td>
            <td width="30%">
                <IMG alt=MTP heigh=500 src="/static/mtpinfoshare/image.jpg" width=80%></IMG>
                <hr>
                <IMG alt=MTP heigh=500 src="/static/mtpinfoshare/image2.jpg" width=80%></IMG>
            </td>
            <td width="35%">&nbsp;</td>
        </tr>
    </table>

</div>
</template>

<script>
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 
    export default {
  name: 'home',
  components: {
    
    
  },
  data:function(){
    return{api_root:api_root}
  },
}
</script>
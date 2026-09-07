import courses from './courses.json';
export type Course=typeof courses[number];
export type Meeting={key:string;course:Course;pattern:Course['patterns'][number];rooms:string[];date:string};
export const iso=(d:Date)=>d.toISOString().slice(0,10);
export const addDays=(d:string,n:number)=>{const x=new Date(d+'T12:00:00Z');x.setUTCDate(x.getUTCDate()+n);return iso(x)};
export const monday=(d:string)=>addDays(d,-((new Date(d+'T12:00:00Z').getUTCDay()+6)%7));
export const time=(n:number)=>`${Math.floor(n/60)%12||12}:${String(n%60).padStart(2,'0')} ${n<720?'AM':'PM'}`;
export function occurrences(date:string,term:number):Meeting[]{
 const results:Meeting[]=[]; const day=(new Date(date+'T12:00:00Z').getUTCDay()+6)%7;
 for(const c of courses.filter(c=>c.term===term))for(const p of c.patterns){
  if(date<p.start||date>p.end||!p.days.includes(day))continue;
  const elapsed=Math.round((Date.parse(date)-Date.parse(p.start))/86400000);
  if(p.alternate&&Math.floor(elapsed/7)%2!==0)continue;
  const key=`${c.id}-${date}-${p.fromMin}-${p.building}`;const old=results.find(m=>m.key===key);
  if(old){if(p.room&&!old.rooms.includes(p.room))old.rooms.push(p.room)}else results.push({key,course:c,pattern:p,rooms:p.room?[p.room]:[],date});
 }
 return results.sort((a,b)=>a.pattern.fromMin-b.pattern.fromMin);
}

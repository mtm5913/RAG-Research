import { defineConfig } from 'vitepress'
export default defineConfig({
 title:'RAG Research', description:'Megan McNeal’s research notebook for source-supported answers: sources, comparisons, learning, experiments and peer review.',
 base:process.env.SITE_BASE || '/RAG-Research/', cleanUrls:false, appearance:false,
 head:[['meta',{name:'theme-color',content:'#e7eff2'}]],
 themeConfig:{siteTitle:'RAG Research',
 nav:[{text:'Overview',link:'/overview'},{text:'Research',link:'/research'},{text:'Sources & tutorials',link:'/sources'},{text:'Experiments',link:'/experiments'},{text:'Partner review',link:'/review'},{text:'Next steps',link:'/roadmap'}],
 socialLinks:[{icon:'github',link:'https://github.com/mtm5913'}],outline:[2,3],search:{provider:'local'},
 footer:{message:'Source facts, proposed decisions, and observed results are recorded separately.',copyright:'Megan McNeal · RAG research · Learning notebook · November 13, 2026'} }
})

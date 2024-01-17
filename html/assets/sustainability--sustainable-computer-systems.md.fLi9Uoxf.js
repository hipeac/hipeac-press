import{_ as e,o as t,c as a,R as i}from"./chunks/framework.tzssv0c6.js";const o="/assets/image1.S_SLG4jl.png",n="/assets/image2.bB_NP8gj.png",b=JSON.parse('{"title":"Sustainable computer systems","description":"","frontmatter":{"title":"Sustainable computer systems\\n","authors":"Lieven Eeckhout","keywords":"sustainability","lastUpdated":"2024-02-05T09:21:00.603Z","prev":{"text":"Sustainable materials and production\\n","link":"/sustainability--sustainable-materials-and-production"},"next":false},"headers":[],"relativePath":"sustainability--sustainable-computer-systems.md","filePath":"sustainability--sustainable-computer-systems.md"}'),r={name:"sustainability--sustainable-computer-systems.md"},s=i('<a target="_blank" href="https://doi.org/10.5281/zenodo.10875174"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.10875174.svg" alt="DOI" class="badge"></a><blockquote><p>Embodied emissions will soon be more significant than operational emissions.</p></blockquote><h1 id="towards-sustainable-computer-systems" tabindex="-1">Towards sustainable computer systems <a class="header-anchor" href="#towards-sustainable-computer-systems" aria-label="Permalink to &quot;Towards sustainable computer systems&quot;">​</a></h1><p>by Lieven Eeckhout</p><p>Sustainability and climate change are a major challenge for our generation. Reducing the environmental footprint of computing implies that we consider the entire life cycle of computer systems including the embodied footprint (manufacturing and production) and operational footprint (device use). Analysing current trends reveals that the embodied footprint is, or will soon be, more significant than the operational footprint. To overcome the inherent data uncertainty regarding sustainability, this article advocates the use of a first-order model to assess the environmental impact of design decisions computer engineers and scientists can make based on first principles. This article further illustrates how this model enables making design trade-offs (in both hardware and software) to reduce the environmental impact of computer systems.</p><h2 id="key-findings" tabindex="-1">Key findings <a class="header-anchor" href="#key-findings" aria-label="Permalink to &quot;Key findings&quot;">​</a></h2><ul><li><p>Improving computing-system sustainability is <strong>more involved than minimizing carbon emissions during production and usage</strong>. Material use (including rare-earth elements and/or minerals from politically unstable regions in the world) and ultra-pure water consumption are significant sustainability concerns related to chip production. <strong>Even if all the energy consumed during production and use were green, the environmental impact of computing would still be significant, and growing</strong>.</p></li><li><p>The environmental footprint of computing continues to grow under current scaling trends. When focusing on carbon emissions, embodied emissions are, or will soon become, the biggest contributor compared to operational emissions across the broad range of computing devices.</p></li><li><p><strong>Embodied emissions are growing</strong> at a fast pace because of <strong>increasing demand for chips</strong> and <strong>increasing energy intensity of semiconductor manufacturing</strong>. Perhaps contradictory to popular belief, improving the energy efficiency of computing systems does not necessarily make them more sustainable.</p></li><li><p>Improving the energy and power efficiency of computing systems may lead to a rebound effect (Jevons paradox) which may be counterproductive to the environmental impact if the resulting <strong>increase in demand outweighs the efficiency improvement</strong>.</p></li><li><p>Improving computing-system sustainability requires a holistic approach to computer architecture design and development, requiring multi-dimensional optimization including chip area, power, energy, performance.</p></li><li><p>A first-order model enables making and assessing design trade-offs to reduce the environmental footprint of computing despite the inherent data uncertainty.</p></li><li><p><strong>There is a role to be played for both hardware and software</strong> to make computer systems more sustainable (or at least less unsustainable).</p></li></ul><h2 id="key-recommendations" tabindex="-1">Key recommendations <a class="header-anchor" href="#key-recommendations" aria-label="Permalink to &quot;Key recommendations&quot;">​</a></h2><ul><li><p>Computer architects should take a holistic approach when designing sustainable computer systems, and not solely focus on carbon emissions.</p></li><li><p>Computer architects and engineers should primarily focus on <strong>reducing the embodied footprint of computer systems</strong>. Reducing the operational footprint is of secondary importance, although still significant.</p></li><li><p>Decarbonizing the manufacturing process is not a panacea as it does not affect other sustainability concerns related to material use and extraction, chemicals and gases emitted, and ultra-pure water consumed during production.</p></li><li><p>Computer scientists and engineers should be wary of <strong>Jevons paradox</strong>. <strong>Efficiency improvements most often lead to a significant rebound effect</strong>. Collaborating with entrepreneurs may yield new, <strong>more sustainable business models</strong> for computing.</p></li><li><p>Computer architects should collaborate with various partners along the supply chain, user groups, and end-of-life recyclers to obtain <strong>high-quality data to assess the environmental impact of raw material extraction, manufacturing, production, assembly, transportation, product use, maintenance, recycling</strong>, etc.</p></li><li><p><strong>Sustainability modeling tools</strong> (both detailed models and high-abstraction analytical models) need to be developed, finetuned and validated to be able to <strong>holistically balance the embodied and operational footprint</strong> of computing devices.</p></li><li><p><strong>Existing and emerging architecture paradigms</strong> (multi-core processing, hardware specialization, core microarchitecture, speculation, chiplet-based integration, etc.) need to be <strong>assessed and re-evaluated from a sustainability perspective</strong>.</p></li></ul><h2 id="sustainability-versus-climate-change" tabindex="-1">Sustainability versus climate change <a class="header-anchor" href="#sustainability-versus-climate-change" aria-label="Permalink to &quot;Sustainability versus climate change&quot;">​</a></h2><p>Climate change is one of the grand challenges of our generation. The recent United Nations Climate Change report [1] in preparation for COP 28, the Dubai Climate Change Conference in November-December 2023, alerts that “<em>national climate action plans remain insufficient to limit global temperature rise to 1.5 degrees Celsius and meet the goals of the Paris Agreement</em>”. While countries are making progress to trend down global greenhouse gas (GHG) emissions, current efforts are insufficient to limit global temperature rise to 1.5 °C by the end of the century. Much more effort is needed to keep this threshold within reach: “<em>greenhouse gas emissions need to be cut 43% by 2030, compared to 2019 levels</em>”.</p><p>Virtually all economic sectors contribute to global emissions. The five economic sectors that contribute most to GHG emissions are industry, electricity, agriculture, transportation and buildings, accounting for nearly 90% of emissions, according to the Organization for Economic Co-operation and Development (OECD) [2]. Freitag et al. [3] recently reported that information and communication technology (ICT) is estimated to contribute 2.1% to 3.9% of worldwide GHG emissions – on par with the aviation industry – and this contribution is rising. As computer scientists and engineers, it is our responsibility to limit ICT’s contribution to global warming, and, if possible, even decrease it.</p><p>While climate change is receiving increasingly wide attention – rightfully so! – it is important that we keep the broader picture in mind when reasoning about potential solutions. The broader picture relates to sustainability. The Brundtland report of the World Council on Economic Development from 1987 provides a broad, yet useful, definition of sustainability: “<em>Sustainable development is development that meets the needs of the present without compromising the ability of future generations to meet their own needs.</em>” This definition is an extremely powerful and unambiguous statement. It is a call for action for our generation: when generating economic activity and developing new devices and services, we should be wary of the impact this may have on future generations.</p><p>Sustainability hence relates to the efficient use of materials and energy, the environmental impact, water consumption, biodiversity, (socio-)economics, impact on human health, human rights, politics, policy, legislation, etc. Global warming is an important aspect of sustainable development, but it should not be the only focus. The extraction and use of raw materials and energy sources is another important aspect of sustainability. What to do when devices reach their end of life and how to repurpose e-waste is equally critical. Sustainability also affects and may require new legislation and business models to reduce pressure on raw-material extraction and to incentivize a circular economy with a reduced environmental footprint.</p><p>Unfortunately, sustainable development in computing is often narrowed down to reducing energy consumption and/or transitioning towards green energy sources. However, making our computer systems more sustainable is much more involved than reducing energy consumption and/or using green energy. Carbon-free computing does not necessarily bring us to a more sustainable future. It is critically important to look at the bigger picture and incorporate the total environmental footprint. For example, Acun et al. [4] point out that a data centre that operates solely on renewable energy does not minimize the total carbon footprint because of the large number of solar panels, wind farms, and batteries needed to enable carbon-free operation. The reason is that the embodied carbon emissions to produce and manufacture the renewable-energy devices (solar panels, wind farms and batteries) outweigh the operational carbon emissions saved during the lifetime of the data centre. This implies that, to minimize the total carbon footprint of a data centre, a more holistic approach is needed that accounts for both the embodied and operational emissions, rather than just focusing on the operational side.</p><h2 id="rebound-effects" tabindex="-1">Rebound effects <a class="header-anchor" href="#rebound-effects" aria-label="Permalink to &quot;Rebound effects&quot;">​</a></h2><p>A necessary condition to reduce the environmental footprint of computing is to make our devices more carbon-efficient, i.e., manufacturing and using a computing device should incur fewer GHG emissions. Unfortunately, while making devices more carbon-efficient is a necessary condition, it is not a sufficient condition because of potential rebound effects. For example, reducing the energy (or carbon) intensity of a device or service typically leads to a price reduction, which in turn stimulates consumption. If the increased consumption outweighs the energy intensity reduction, we end up with a net increase in environmental impact – exactly opposite of what we had envisioned! This is the well-known Jevons Paradox, named after Williams Stanley Jevons, who was the first to observe the rebound effect of the steam engine’s improved coal efficiency leading to an overall increase in coal consumption [5]. Applied to computing, improving the energy or power efficiency of a computing device does not necessarily lead to a net reduction in environmental impact. Most often, an energy- or power-efficiency gain leads to increased usage and deployment, effectively increasing the environmental impact of computing. For example, a more power-efficient server incentivizes data centre operators to host more servers within the data centre’s power envelop, which (may) lead(s) to an increased embodied and operational footprint. Mitigating this rebound effect might need new business models and/or legislation and regulation to make sure that the reduction in per-device emissions leads to an overall decrease in emissions across all devices.</p><h2 id="understanding-trends-in-environmental-impact-of-computing" tabindex="-1">Understanding trends in environmental impact of computing <a class="header-anchor" href="#understanding-trends-in-environmental-impact-of-computing" aria-label="Permalink to &quot;Understanding trends in environmental impact of computing&quot;">​</a></h2><p>Before discussing what we, computer engineers and computer scientists, can do to reduce the environmental footprint of computing, it is important that we understand what the current trends look like. To do so, we make a distinction between embodied versus operational emissions [6]. (For the discussion that follows, we will mostly focus on GHG emissions, but several aspects also pertain to other environmental concerns, such as raw material extraction, water consumption, etc.)</p><p>Embodied emissions relate to raw-material extraction, manufacturing, assembly, transportation, repair, maintenance, and end-of-life processing. Operational emissions relate to product use during a device’s lifetime. Embodied emissions can be further categorized in scope-1, scope-2, and scope-3. Scope-1 refers to the chemicals and gases used during manufacturing – this includes fluorinated greenhouse gases with orders of magnitude higher global warming potential than CO<sub>2</sub>. Scope-2 refers to the energy consumption during chip manufacturing – this includes empowering the extensive production facilities with hundreds of manufacturing tools and requiring climate and humidity control. Scope-3 pertains to the energy consumption for the extraction and production of materials used for integrated circuit manufacturing.</p><p>Gupta et al. [6] performed a comprehensive survey of consumer devices from vendors including Apple, Google, Huawei, and Microsoft. They conclude that embodied emissions dominate for battery-operated devices such as wearables, smartphones, tablets, and laptops, while operational emissions dominate for always-connected devices such as speakers, desktop computers and gaming consoles. For data centres, most emissions are related to construction, infrastructure, and hardware manufacturing: interestingly, while total energy usage is trending up – presumably because of increased server count and/or higher degree of consolidation (cf. Jevons paradox) – total operational emissions are decreasing for Facebook and Google, thanks to their policy of contracting and securing green energy sources to power their hyperscale data centres.</p><p>Eeckhout reformulated the well-known Kaya identity to project how the environmental footprint computing will change into the future [11]. The overall conclusion from this analysis is that the embodied emissions are continuing to grow under current scaling trends, and that embodied emissions already are, or will soon be, the biggest contributor. The fundamental reason is the increasing demand for chips (because of economic dynamics based on selling products, i.e., linear economy) and the growing energy intensity of semiconductor manufacturing (because of advancements in chip technology), which do not seem to be counterbalanced by the transition to green energy sources and improvements in per-device energy and power efficiency.</p><h2 id="inherent-data-uncertainty" tabindex="-1">Inherent data uncertainty <a class="header-anchor" href="#inherent-data-uncertainty" aria-label="Permalink to &quot;Inherent data uncertainty&quot;">​</a></h2><p>A major challenge when doing research in sustainable computing is the high degree of uncertainty along a variety of dimensions. While companies’ sustainability reports and product lifecycle-assessment (LCA) reports provide a wealth of data, there remain many unknowns and data limitations, in part because of industry secretiveness, or simply because of lack of reliable data. For example, a recent study by imec [7], which attempts to quantify the environmental footprint of modern-day chip manufacturing, makes assumptions regarding the energy consumption of a fab’s facility equipment (i.e. it is “<em>assumed to contribute to 40% of the total energy</em>”); furthermore, the degree of abatement of fluorinated GHGs (scope-1) is unknown, as well as the use of materials and the energy needed for material extraction (scope-3). As another example, the Apple iPhone12 LCA report [8] uses industry averages when parameters are unknown for the production process, i.e. a company may not know the sustainability impact of its suppliers.</p><p>The operational footprint and its importance relative to the embodied footprint is even harder to assess, as it depends on typical user behaviour, product lifetime, and the geographic location of the user (which determines the carbon intensity of the user’s power grid mix). Historical data could be insightful, but it only provides a hint. Note further that product use may be subject to the infamous rebound effect, which may significantly shift the relative importance of the operational versus embodied footprint.</p><p>Overall, it is safe to conclude that there is inherent data uncertainty. Gupta et al. [9] recently proposed the ACT model to analyse a computer system’s sustainability at design time. This model relies on detailed numbers from production processes in industry. This is an important step for our community at large (both in industry and academia). Nevertheless, the authors note that there is “<em>lack of up-to-date carbon emission data for the latest compute, memory, and storage technologies</em>”. Furthermore, they hope to “<em>encourage industry to publish more detailed carbon characterizations to standardize carbon footprint accounting</em>”. Imec’s sustainable semiconductor technology and systems (SSTS) program aims at addressing exactly this issue by collaborating with major industry players to quantify the environmental impact of integrated circuit manufacturing [10].</p><h2 id="sustainable-design-based-on-first-principles" tabindex="-1">Sustainable design based on first principles <a class="header-anchor" href="#sustainable-design-based-on-first-principles" aria-label="Permalink to &quot;Sustainable design based on first principles&quot;">​</a></h2><p>And yet, despite the large degrees of uncertainty and the multi-faceted design problem, computer engineers and scientists need to make computer systems more sustainable. A potential solution is to revert to first principles and guide sustainable design decisions using a first-order model. First-order modelling should not be viewed as a replacement for, but rather as a useful complement to, detailed models like ACT and others. In fact, a detailed sustainability accounting method can provide initial data for a first-order model, and vice versa, a first-order model can provide directions where the detailed model should be further refined.</p><p>A first-order model uses proxies for the embodied and operational footprint that computer architects have control over, see for example [12] for more details about a first-order model for processor chips. A useful, first-order proxy for the embodied footprint of a chip is its die size, i.e. the larger the chip, the higher the embodied footprint for a given chip technology in terms of the energy and materials needed and the chemicals and gases emitted during production of the chip. A useful proxy for the operational footprint of a chip is energy consumption assuming a fixed-work scenario (i.e. a device performs a fixed amount of work during its entire lifetime) and power consumption assuming a fixed-time scenario (i.e. a device is used for the same amount of time, and hence performs more work). The relative importance of embodied versus operational emissions can be captured via a parameter α which the architect can vary to explore different use case scenarios.</p><h2 id="what-can-we-on-the-hardware-side" tabindex="-1">What can we on the hardware side? <a class="header-anchor" href="#what-can-we-on-the-hardware-side" aria-label="Permalink to &quot;What can we on the hardware side?&quot;">​</a></h2><p>Although (deliberately) simple, a first-order sustainability model can reveal a variety of interesting insights which computer architects can take forward to design more sustainable computer systems despite the inherent data uncertainty. There is a fruitful avenue of future work to explore how computer architectures can be made more sustainable. We provide three examples here to illustrate the trade-offs one can make using the first-order model. Expanding and analysing to what extent a broader range of archetypal CPU and GPU design paradigms and solutions (e.g. caching, speculation, microarchitecture, acceleration, etc.) affect computer system sustainability would be extremely valuable.</p><p><img src="'+o+'" alt=""><em>Figure : Total carbon footprint of a general-purpose CPU plus accelerator as a function of its degree of use, assuming that the accelerator takes up 6.5% extra chip area (left) versus 2x extra chip area (right), normalized to a general-purpose CPU without an accelerator. The accelerator is assumed to consume 500x less energy than the general-purpose CPU for performing the same work. Two scenarios are considered: embodied emissions account for 80% of total emissions versus 20% of total emissions. The larger the chip area of the accelerator, the more frequently it needs to be used and the higher the relative weight of the operational emissions need to be for the accelerator to be sustainable. Taken from [4].</em></p><h3 id="hardware-specialisation-and-dark-silicon" tabindex="-1">Hardware specialisation and dark silicon <a class="header-anchor" href="#hardware-specialisation-and-dark-silicon" aria-label="Permalink to &quot;Hardware specialisation and dark silicon&quot;">​</a></h3><p>As reported in [12], the first-order model can be used to assess whether hardware specialization is sustainable. Integrating a hardware accelerator next to a general-purpose processor incurs a cost in terms of embodied footprint (because of a larger chip) which may be compensated for by the reduced operational footprint (because of lower energy consumption when using the special-purpose accelerator rather than a general-purpose CPU). In other words, the reduced operational footprint amortizes the increased embodied footprint.</p><p>The question is where the tipping point is. The larger the accelerator, the more frequently the accelerator needs to be used and the higher the relative weight of the operational emissions needs to be for the accelerator design to be sustainable, as illustrated in Figure 1, if the accelerator is taking up significant chip area, and the embodied emissions dominate, the reduction in operational emissions does not compensate for the increased embodied emissions.</p><p>This suggests that the current trend towards large system-on-chip (SoC) designs with dozens of accelerators that occupy a significant fraction of the chip and that are not powered on all the time due to dark-silicon constraints, may not be a sustainable design paradigm. A more fruitful, sustainable design paradigm might be to consolidate accelerator designs to a common-denominator accelerator that can serve multiple critical applications while incurring less chip area, thereby reducing the embodied footprint at the expense of an increased operational footprint, with a net improvement in sustainability.</p><h3 id="core-microarchitecture" tabindex="-1">Core microarchitecture <a class="header-anchor" href="#core-microarchitecture" aria-label="Permalink to &quot;Core microarchitecture&quot;">​</a></h3><p>A second example, also taken from [12], considers four microarchitectures: (1) a low-power in-order (InO) core; (2) a high-performance out-of-order (OoO) core; (3) a Forward Slice Core (FSC) [13], a complexity-effective core microarchitecture that aims for a level of performance that is comparable to OoO while incurring a small area and power overhead compared to InO; and (4) an OoO core enhanced with Precise Runahead Execution (PRE) [14], an efficient hardware data prefetching technique.</p><p>Figure 2 reports the total normalized carbon footprint for these microarchitectures as a function of performance considering different scenarios: fixed-work versus fixed-time and embodied versus operational emissions dominating. Ideally, a microarchitecture should be situated in the bottom right: high performance at low environmental footprint. Several interesting conclusions can be reached from this analysis. First, some microarchitectures are clearly better than others, possibly under (a) specific scenario(s). For example, under a fixed-work scenario (subfigures a and b), FSC and PRE are clearly better design options than InO and OoO, respectively, because they achieve higher performance at a lower environmental footprint. Second, different microarchitectures offer different trade-offs. For example, while PRE yields higher performance than FSC, it also incurs a higher environmental footprint. Third, whether a microarchitecture incurs a lower environmental footprint may depend on the scenario. While PRE reduces the environmental footprint compared to OoO under a fixed-work scenario (subfigures a and b), it incurs a (much) higher footprint under a fixed-time scenario. This suggests that PRE is subject to a rebound effect: because PRE yields higher performance, it can perform more work in the same amount of time, which, because of its higher power consumption, leads to a higher operational footprint, and as a result a higher overall footprint.</p><p><img src="'+n+'" alt=""><em>Figure : Comparing the OoO, Ino, FSC, and PRE microarchitectures in terms of normalised carbon footprint as a function of performance, assuming a fixed-work scenario (subfigures a and b) and fixed-time scenarioj (subfigures c and d) for different values for α, i.e. when the embodied footprint dominates (subfigures a and c) and when the operational footprint dominates (subfigures b and d). Taken from [12].</em></p><h3 id="chiplet-based-integration" tabindex="-1">Chiplet-based integration <a class="header-anchor" href="#chiplet-based-integration" aria-label="Permalink to &quot;Chiplet-based integration&quot;">​</a></h3><p>A third timely architecture trade-off worth exploring in the context of sustainability relates to chiplet-based integration. Small chiplets improve manufacturing yield, which reduces the amount of waste, and thus also the effective embodied footprint per correctly operating chiplet. Chiplet-based integration hence does not only reduce cost, but it also has the potential to improve sustainability [15]. Heterogeneous integration of chiplets manufactured in different chip technology nodes could possibly further reduce the environmental footprint because older tech nodes incur a lower environmental footprint for the same chip area [7]. On the flip side, chiplet integration requires a silicon interposer or organic substrate with silicon bridges to connect the chiplets; these integration technologies and substrates obviously incur an additional environmental cost. When looking at the full picture, it is unclear whether homogeneous and/or heterogeneous chiplet integration reduces or increases the environmental footprint. Investigating these (and other) architecture trade-offs is a promising research avenue for computer engineers in industry and academia.</p><h2 id="what-can-we-do-on-the-software-side" tabindex="-1">What can we do on the software side? <a class="header-anchor" href="#what-can-we-do-on-the-software-side" aria-label="Permalink to &quot;What can we do on the software side?&quot;">​</a></h2><p>Reducing the environmental footprint of computing is not only a job for computer engineers – computer scientists can also contribute. In other words, this is not just a hardware problem, and software could be part of the solution. Of course, and most obviously, developers and researchers on the software side could (and should) aim for reducing the amount of energy and power consumed by software on existing (and future) hardware. This is a no-brainer, but it only affects the operational footprint of a computer system. There is an opportunity for software to also reduce the embodied footprint of computing. Two examples illustrate this.</p><h3 id="low-overhead-programming-languages" tabindex="-1">Low-overhead programming languages <a class="header-anchor" href="#low-overhead-programming-languages" aria-label="Permalink to &quot;Low-overhead programming languages&quot;">​</a></h3><p>Pereira et al. [16] study the energy efficiency and memory consumption of a broad variety of programming languages. They conclude that high-abstraction, managed programming languages consume substantially more energy and memory than low-level, natively compiled programming languages. For example, they find that Python and Java consume 75x and 2x more energy, and 2.4x and 5.1x more memory compared to C, respectively. This implies that there is a direct reduction in operational footprint to be achieved by implementing software in native languages rather than managed languages. But there is also an indirect reduction to be exploited: software written in native languages can run as efficiently on less powerful hardware (with less compute and memory capacity). Because the less powerful hardware incurs a smaller embodied footprint, this could lead to overall reduction in environmental footprint. Of course, there are many more design goals to consider than just performance and sustainability, including software productivity and security, but at least this example illustrates that there is a potential for reducing the environmental footprint of computing by reverting to low-overhead programming languages and/or by reducing the run-time overhead in (managed) programming languages.</p><h3 id="parallelisation" tabindex="-1">Parallelisation <a class="header-anchor" href="#parallelisation" aria-label="Permalink to &quot;Parallelisation&quot;">​</a></h3><p>In a similar way, parallelising software has the potential to temper the need for ever more powerful multicore processors with increasing number of cores. A simple calculation using Amdahl’s Law illustrates this. A multicore processor with 16 cores running software where 95% of the serial execution has been parallelised yields 17% higher performance compared to a multicore processor with 32 cores running software where 90% of the serial execution has been parallelised. The 32-core processor incurs a higher embodied footprint because the chip is (approximately) twice as big as the 16-core processor, and yet it achieves higher performance. The reason is that software is (slightly) more parallel. In other words, parallelising software is a more sustainable way to improve performance than increasing core count. Of course, parallelising software is challenging but, if successful, it can lead to an overall footprint reduction.</p><h2 id="conclusion" tabindex="-1">Conclusion <a class="header-anchor" href="#conclusion" aria-label="Permalink to &quot;Conclusion&quot;">​</a></h2><p>Improving computing-system sustainability is a challenging and multi-faceted problem. The embodied footprint is, or will soon be, a more important contributor than the operational footprint, primarily due to an increasing demand for chips and increased energy intensity of integrated circuit manufacturing. Decarbonizing the production process and use phase of compute devices is not a panacea, though, because it does not address other sustainability concerns including raw material extraction, chemicals and gases emitted, and ultra-pure water used during production.</p><p>What makes sustainable computer system design unique compared to traditional optimization criteria is that it requires a holistic approach considering chip area, power, energy, performance. The field of computer architecture specifically, and computer science and engineering in general, has only recently embarked on this endeavour.</p><p>Computer architects should continue to (1) collect high-quality data to assess the sustainability impact across the entire lifetime of a computing device, from raw-material extraction, transportation, manufacturing, assembly, use, repair, end-of-life processing, etc., (2) develop detailed and high-abstraction models to help designers evaluate the impact on sustainability at design time, and (3) analyse and revisit architecture design paradigms considering their sustainability impact. Overall, sustainable system design is an extremely timely and societally important topic where substantial innovation is to be achieved and expected in the following years.</p><p>References</p><div class="info custom-block"><p class="custom-block-title">AUTHOR</p><p><strong>Lieven Eeckhout</strong> is a senior full professor in the department of electronics and information systems at Ghent University, Belgium.</p></div><div class="info custom-block"><p class="custom-block-title">REFERENCES</p><p>[1]: “Climate Plans Remain Insufficient: More Ambitious Action Needed Now,” United Nations, 26 October 2022. [Online]. Available: <a href="https://unfccc.int/news/climate-plans-remain-insufficient-more-ambitious-action-needed-now" target="_blank" rel="noreferrer">https://unfccc.int/news/climate-plans-remain-insufficient-more-ambitious-action-needed-now</a>. [Accessed 28 November 2022].<br> [2]: “Climate Action Explore policy solutions by key economic sector,” OECD, [Online]. Available: <a href="https://www.oecd.org/stories/climate-action/key-sectors/" target="_blank" rel="noreferrer">https://www.oecd.org/stories/climate-action/key-sectors/</a> . [Accessed 28 November 2022].<br> [3]: C. Freitag, M. Berners-Lee, K. Widdicks, B. Knowles, G. S. Blair, A. Friday, “The Real Climate and Transformative Impact of ICT: A Critique of Estimates, Trends, and Regulations,” Patterns, vol. 2, no. 9, pp. 100340, <a href="https://doi.org/10.1016/j.patter.2021.100340" target="_blank" rel="noreferrer">https://doi.org/10.1016/j.patter.2021.100340</a>, 2021.<br> [4]: B. Acun, B. Lee, K. Maeng, M. Chakkaravarthy, U. Gupta, D. Brooks, C.-J. W, “Carbon Explorer: A Holistic Approach for Designing Carbon-Aware Datacenters,” in ACM International Conference on Architecture Support for Programming Languages and Operating Systems (ASPLOS), Vancouver, 2023.<br> [5]: “W. Stanley Jevons, “The Coal Question,” 1865,” Yale University, [Online]. Available: <a href="https://energyhistory.yale.edu/library-item/w-stanley-jevons-coal-question-1865" target="_blank" rel="noreferrer">https://energyhistory.yale.edu/library-item/w-stanley-jevons-coal-question-1865</a>. [Accessed 28 November 2022].<br> [6]: U. Gupta, Y. G. Kim, S. Lee, J. Tse, H.-H. S. Lee, G.-Y. Wei, D. Brooks, C.-J. Wu, “Chasing Carbon: The Elusive Environmental Footprint of Computing,” in IEEE International Symposium on High-Performance Computer Architecture (HPCA), Virtual, 2021.<br> [7]: M. Garcia Bardon, P. Wuytens, L.-A. Ragnarsson, G. Mirabelli, D. Jang, G. Willens, A. Mallik, S. Spessot, J. Ryckaert, B. Parvais, “DTCO including Sustainability: Power-Performance-Area-Cost-Environmental score (PPACE) Analysis for Logic Technologies,” in 2020 IEEE International Electron Devices Meeting (IEDM), Virtual, 2020.<br> [8]: “Product Environmental Report: iPhone 12,” 13 October 2020. [Online]. Available: <a href="https://www.apple.com/environment/pdf/products/iphone/iPhone_12_PER_Oct2020.pdf" target="_blank" rel="noreferrer">https://www.apple.com/environment/pdf/products/iphone/iPhone_12_PER_Oct2020.pdf</a> .<br> [9]: U. Gupta, M. Elgamal, G. Hills, G.-Y. Wei, H.-H. S. Lee, D. Brooks, C.-J. Wu, “ACT: Designing Sustainable Computeer Systems with an Architectural Carbon Modeling Tool,” in ISCA &#39;22: Proceedings of the 49th Annual International Symposium on Computer Architecture, New York, 2022.<br> [10]: L.-A. Ragnarsson, C. Rolin, S. Shamuilia, E. Parton, “The green transition of the IC industry,” Imec, [Online]. Available: <a href="https://www.imec-int.com/en/expertise/cmos-advanced/sustainable-semiconductor-technologies-and-systems-ssts/stss-white-paper" target="_blank" rel="noreferrer">https://www.imec-int.com/en/expertise/cmos-advanced/sustainable-semiconductor-technologies-and-systems-ssts/stss-white-paper</a>. [Accessed 28 November 2022].<br> [11]: L. Eeckhout, “Kaya for Computer Architects: Towards Sustainable Computer Systems,” IEEE Micro, pp. 1-8, <a href="https://ieeexplore.ieee.org/document/9932869" target="_blank" rel="noreferrer">https://ieeexplore.ieee.org/document/9932869</a>, 2022.<br> [12]: L. Eeckhout, “A First-Order Model to Assess Computer Architecture Sustainability,” IEEE Computer Architecture Letters, vol. 21, no. 2, pp. 137-40, July-Dec 2022.<br> [13]: <a href="https://dl.acm.org/doi/10.1145/3410463.3414629" target="_blank" rel="noreferrer">https://dl.acm.org/doi/10.1145/3410463.3414629</a><br> [14]: <a href="https://ieeexplore.ieee.org/document/9065552" target="_blank" rel="noreferrer">https://ieeexplore.ieee.org/document/9065552</a><br> [15]: <a href="https://www.computer.org/csdl/journal/ca/2023/02/10244005/1QgWSmqbYt2" target="_blank" rel="noreferrer">https://www.computer.org/csdl/journal/ca/2023/02/10244005/1QgWSmqbYt2</a><br> [16]: <a href="https://dl.acm.org/doi/10.1145/3136014.3136031" target="_blank" rel="noreferrer">https://dl.acm.org/doi/10.1145/3136014.3136031</a></p></div>',55),c=[s];function l(d,u,h,m,p,f){return t(),a("div",null,c)}const y=e(r,[["render",l]]);export{b as __pageData,y as default};
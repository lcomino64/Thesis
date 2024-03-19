```markdown
digraph G {

    rankdir=LR;

    node [shape=record];

  

    subgraph cluster_0 {

        label="Local Network";

        FPGA [label="FPGA and Peripherals"];

        Switch [label="Switch"];

        MC1 [label="Micro-Computer 1"];

        MC2 [label="Micro-Computer 2"];

    }

  

    Router [label="Router"];

    Internet [label="Internet"];

  

    MC1 -> Switch;

    MC2 -> Switch;

    FPGA -> Switch;

    Switch -> Router;

    Router -> Internet;

}
```
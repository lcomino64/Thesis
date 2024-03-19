```markdown
digraph G {

    rankdir=LR;

    node [shape=record];

  

    subgraph cluster_0 {

        C1 [label="Core 0: Main CPU"];

        T1 [label="Core 1: TCP/IP Stack"];

        subgraph cluster_1 {

            label="Shared Memory";

            SM [label="Shared Memory Block"];

        }

    }

  

    subgraph cluster_1 {

        label="Peripherals"

        P1 [label="VGA, GPIO etc."];

    }

  

    P2 [label="Ethernet"];

  

    C1 -> SM;

    C1 -> P1;

  

    T1 -> SM;

    T1 -> P2;

}
```
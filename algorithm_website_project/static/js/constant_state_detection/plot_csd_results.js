// function to plot constant section
// detection results

window.plot_csd_results_1 = function(
   xData, yData, startData, finishData,
   startSectionData, finishSectionData,
   div_id
)
{
    y_max = Math.max(...yData);
    y_min = Math.min(...yData);
    y_mid = (y_max + y_min) / 2.0
    // plotly.js add to plot
    // some semitransparent rectangles

    // array for rectangles
    const shapes_arr = [];

    // add start and finish detected
    // constant sections rectangles
    for (let i = 0; i < startData.length;
         i++)
    {
        fig =  {
                  type: 'rect',
                  // Coordinates for the rectangle (using data coordinates)
                  x0: xData[startData[i]],
                  y0: y_mid,
                  x1: xData[finishData[i]],
                  y1: y_max,
                  // Use rgba for transparency (e.g., 16% opacity)
                  fillcolor: 'rgba(255, 0, 0, 0.16)',
                  line: {
                    color: 'rgba(255, 0, 0, 0.48)',
                    width: 1
                  }
                }
        if( i === 0)
        {
            fig.showlegend = true;
            fig.name = "Chosen constant sections"
        }

        shapes_arr.push(fig)
    }

    // add start and finish
    // continuous constant section
    // series rectangles
    for (let i = 0;
         i < startSectionData.length;
         i++)
    {
        fig = {
                  type: 'rect',
                  // Coordinates for the rectangle (using data coordinates)
                  x0: xData[startSectionData[i]],
                  y0: y_min,
                  x1: xData[finishSectionData[i]],
                  y1: y_mid,
                  // Use rgba for transparency (e.g., 16% opacity)
                  fillcolor: 'rgba(0, 0, 255, 0.16)',
                  line: {
                    color: 'rgba(0, 0, 255, 0.48)',
                    width: 1
                  }
                }
        if( i === 0)
        {
            fig.showlegend = true;
            fig.name = "Region of the uninterrupted constant sections"
        }

        shapes_arr.push(fig);

    }

    // add line to shapes
    mid_line = {
          type: 'line',
          xref: 'x',  // Uses canvas coordinates for X (0 = start, 1 = end)
          yref: 'y',      // Uses data coordinates for Y
          x0: xData[0],          // Absolute start of the plot area
          y0: y_mid,         // The horizontal line's Y-value
          x1: xData[xData.length - 1],          // Absolute end of the plot area
          y1: y_mid,         // Matches y0 to keep it perfectly horizontal
          line:
                {
                    color: 'green',
                    width: 1,
                    dash: 'solid',  // Optional: 'dash', 'dot', or 'solid'
                  },
          showlegend: true,
          name: 'Middle line',
        }

    shapes_arr.push(mid_line)

    const layout = {
        title:
            {
                text: 'The plot of the constant state detection results'
            },
          xaxis:
          {
            title:
            {
              text: 'Time series index'
            }
          },
          yaxis:
          {
            title:
            {
              text: 'Time series value'
            }
          },

        shapes: shapes_arr,
        showlegend: true, // Explicitly force the legend to show
    };

    const trace = {
        x: xData,
        y: yData,
        name: 'Input data',
        mode: 'lines+markers', // Options: 'lines', 'markers', or 'lines+markers'
        type: 'scatter',       // 'scatter' handles line and scatter plots
        marker: { color: 'blue', size: 8 },
        line: { color: 'blue', width: 2 }
    };
    const data = [trace];
    Plotly.newPlot(div_id,
        data, layout);
}

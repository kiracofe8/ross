"""Point mass module.

This module defines the PointMass class which will be used to link elements.
"""
import numpy as np
from ross.element import Element

__all__ = ["PointMass"]


class PointMass(Element):
    """A point mass element.

    This class will create a point mass element.
    This element can be used to link other elements in the analysis.
    The mass provided to the element can be different on the x and y direction
    (e.g. different support inertia for x and y directions).

    Parameters
    ----------
    n: int
        Node which the bearing will be located in.
    m: float, optional
        Mass for the element.
    mx: float, optional
        Mass for the element on the x direction.
    my: float, optional
        Mass for the element on the y direction.

    Examples
    --------
    >>> p0 = PointMass(n=0, m=2)
    >>> p0.M()
    array([[2, 0],
           [0, 2]])
    >>> p1 = PointMass(n=0, mx=2, my=3)
    >>> p1.M()
    array([[2, 0],
           [0, 3]])
    """

    def __init__(self, n=None, m=None, mx=None, my=None, tag=None):
        self.n = n
        self.m = m

        if mx is None and my is None:
            mx = m
            my = m

        self.mx = mx
        self.my = my
        self.tag = tag

    def __hash__(self):
        return hash(self.tag)

    def M(self):
        """Mass matrix."""
        mx = self.mx
        my = self.my
        # fmt: off
        M = np.array([[mx, 0],
                      [0, my]])
        # fmt: on

        return M

    def C(self):
        """Damping coefficients matrix."""
        return np.zeros((2, 2))

    def K(self):
        """Stiffness coefficients matrix."""
        return np.zeros((2, 2))

    def G(self):
        """Gyroscopic matrix."""
        return np.zeros((2, 2))

    def dof_mapping(self):
        return dict(x_0=0, y_0=1)

    def patch(self, position, ax, **kwargs):
        """Point mass element patch.
        Patch that will be used to draw the point mass element.
        Parameters
        ----------
        ax : matplotlib axes, optional
            Axes in which the plot will be drawn.
        position : float
            Position in which the patch will be drawn.
        kwargs : optional
            Additional key word arguments can be passed to change
            the plot (e.g. linestyle='--')
        Returns
        -------
        ax : matplotlib axes
            Returns the axes object with the plot.
        """
        zpos, ypos = position
        radius = ypos / 8

        default_values = dict(alpha=1.0, color=bokeh_colors[7])

        for k, v in default_values.items():
            kwargs.setdefault(k, v)

        # matplotlib plot - coordinates to plot point mass elements
        ax.add_patch(
            mpatches.Circle(xy=(zpos, ypos), radius=radius, **kwargs)
        )
        ax.add_patch(
            mpatches.Circle(xy=(zpos, -ypos), radius=radius, **kwargs)
        )

    def bokeh_patch(self, position, bk_ax, **kwargs):
        """Point mass element patch.
        Patch that will be used to draw the point mass element.
        Parameters
        ----------
        bk_ax : bokeh plotting axes, optional
            Axes in which the plot will be drawn.
        position : float
            Position in which the patch will be drawn.
        kwargs : optional
            Additional key word arguments can be passed to change
            the plot (e.g. linestyle='--')
        Returns
        -------
        bk_ax : bokeh plotting axes
            Returns the axes object with the plot.
        """
        zpos, ypos = position
        radius = ypos / 8

        default_values = dict(
            line_width=2.0,
            line_color=bokeh_colors[0],
            fill_alpha=1.0,
            fill_color=bokeh_colors[7],
            legend="Point Mass",
        )

        for k, v in default_values.items():
            kwargs.setdefault(k, v)

        # bokeh plot - coordinates to plot point mass elements
        z_upper = [zpos]
        y_upper = [ypos]

        z_lower = [zpos]
        y_lower = [-ypos]

        source = ColumnDataSource(
            dict(
                z_l=z_lower,
                y_l=y_lower,
                z_u=z_upper,
                y_u=y_upper,
                elnum=[self.n],
                mx=[self.mx],
                my=[self.my],
                tag=[self.tag],
            )
        )

        bk_ax.circle(
            x="z_l",
            y="y_l",
            radius=radius,
            source=source,
            name="pmass_l",
            **kwargs,
        )
        bk_ax.circle(
            x="z_u",
            y="y_u",
            radius=radius,
            source=source,
            name="pmass_u",
            **kwargs,
        )

        hover = HoverTool(names=["pmass_l", "pmass_u"])
        hover.tooltips = [
            ("Point Mass Node :", "@elnum"),
            ("Mass (x) :", "@mx"),
            ("Mass (y) :", "@my"),
            ("Tag :", "@tag"),
        ]
        hover.mode = "mouse"

        return hover

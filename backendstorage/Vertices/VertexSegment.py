# from backendstorage.Vertices.VertexPoint import VertexPoint
# class VertexSegment:
#     def __init__(self,**kwargs):
#         self.vertexPoints = set()
#
#     def splitVertex(self):
#         newVertexPoint = VertexPoint()
#         newVertexSegment = self.insertVertex(newVertexPoint)
#         return newVertexSegment
#
#     def insertVertex(self, newVertexPoint):
#         pointlist = list(self.vertexPoints)
#         self.vertexPoints.remove(pointlist[1])
#         self.vertexPoints.add(newVertexPoint)
#         newVertexSegment = VertexSegment()
#         newVertexSegment.vertexPoints.add(newVertexPoint)
#         newVertexSegment.vertexPoints.add(pointlist[1])
#         return newVertexSegment
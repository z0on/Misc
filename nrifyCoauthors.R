home="Texas at Austin"
coauthorFile="~/Documents/GRANTS/coauthors2012_2016.txt"

co=read.table(coauthorFile,header=T,sep="\t")
co=co[!is.na(co$Affiliation),]
co=co[-(grep(home,co$Affiliation)),]
str(co)
names=unique(co$Name)
Names=data.frame(matrix(unlist(strsplit(as.character(names),split=", ",fixed=T)),ncol=2,byrow=T))
names(Names)=c("Last","First")
Names$Affiliation=0
for (n in 1:length(names)){
	s=subset(co,Name==names[n])
	Names$Affiliation[n]=as.character(s$Affiliation[1])
}
write.table(Names,file=paste(coauthorFile,".nr.txt",sep=""),quote=F,row.names=F,sep="\t")
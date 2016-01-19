
# this script writes a tab-deimited table of unique coauthor names and affiliations
# If many affiliations exist for a coauthor, the most recent one will be listed.
# coauthors with no listed affiliations are dropped
# by Mikhail Matz, matz@utexas.edu

home="Texas at Austin" # phrase to recognize your home institution - I assuming we don't need to list those coauthors
coauthorFile="~/Documents/GRANTS/coauthors2012_2016.txt" # output of Casey Dunn's script, also available at https://github.com/z0on/Misc/blob/master/fetchCoauthors.py

co=read.table(coauthorFile,header=T,sep="\t")
co=co[!is.na(co$Affiliation),] # remark this line if you want to list coauthors with no listed affiliation
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
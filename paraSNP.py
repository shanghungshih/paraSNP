import sys
import os

num = str(sys.argv[1])
path = os.getcwd()
filename = num+".mutect2.filter.vcf"
in_name = path+'/'+filename
out_name = path+'/'+num+'.paraSNP.vcf'
out = open(out_name, 'w')
with open(in_name, 'r') as f:
    for l in f.readlines():
        if l.count('#') == 0:
            if l.split(sep='\t')[0].split(sep='chr')[1].isnumeric() == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('X') == True or l.split(sep='\t')[0].split(sep='chr')[1].endswith('Y') == True:
                #"""SNV"""
                if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) == 1:
                    #print(l.split(sep='\t')[0].split(sep='chr')[1], l.split(sep='\t')[1], l.split(sep='\t')[1], l.split(sep='\t')[3], l.split(sep='\t')[4], 'OSCC-'+num, sep='\t')
                    w = l.split(sep='\t')[0].split(sep='chr')[1]+'\t'+l.split(sep='\t')[1]+'\t'+l.split(sep='\t')[1]+'\t'+l.split(sep='\t')[3]+'\t'+l.split(sep='\t')[4]+'\t'+'OSCC-'+num+'\n'
                    out.writelines(w)
                #"""deletion"""
                if len(l.split(sep='\t')[3]) != 1 and len(l.split(sep='\t')[4]) == 1:
                    #print(l.split(sep='\t')[0].split(sep='chr')[1], int(l.split(sep='\t')[1])+1, int(l.split(sep='\t')[1])+len(l.split(sep='\t')[3][1:]), l.split(sep='\t')[3][1:], '-', 'OSCC-'+num, sep='\t')
                    w = l.split(sep='\t')[0].split(sep='chr')[1]+'\t'+str(int(l.split(sep='\t')[1])+1)+'\t'+str(int(l.split(sep='\t')[1])+len(l.split(sep='\t')[3][1:]))+'\t'+l.split(sep='\t')[3][1:]+'\t'+'-'+'\t'+'OSCC-'+num+'\n'
                    out.writelines(w)
                #"""insertion"""
                if len(l.split(sep='\t')[3]) == 1 and len(l.split(sep='\t')[4]) != 1:
                    #print(l.split(sep='\t')[0].split(sep='chr')[1], int(l.split(sep='\t')[1]), int(l.split(sep='\t')[1]), '-', l.split(sep='\t')[4][1:], 'OSCC-'+num, sep='\t')
                    w = l.split(sep='\t')[0].split(sep='chr')[1]+'\t'+str(int(l.split(sep='\t')[1]))+'\t'+str(int(l.split(sep='\t')[1]))+'\t'+'-'+'\t'+l.split(sep='\t')[4][1:]+'\t'+'OSCC-'+num+'\n'
                    out.writelines(w)
out.close()

os.system('sudo docker run --rm -v /Users/shanghungshih/Downloads/autoOncotator-master:/data adgh456/parasnp perl annovar/table_annovar.pl data/{}.paraSNP.vcf annovar/humandb/ -buildver hg19 -out data/{}.paraSNP -remove -protocol refGene,ljb26_all -operation g,f -nastring NA -otherinfo'.format(num, num))

os.system('mv {}/{}.paraSNP.hg19_multianno.txt {}/{}.hg19_multianno.txt'.format(path, num, path, num))

os.system('sudo docker run -itd --rm -v /Users/shanghungshih/Downloads/autoOncotator-master:/data adgh456/parasnp')

os.system('sudo docker ps -l > ParaSNPid.txt')
with open('ParaSNPid.txt', 'r') as f:
    for i in f.readlines():
        if i.startswith('CONTAINER') is False:
            mainID = i.split('        ')[0]
            mainBox = "sudo docker exec "+mainID+' '
os.system('rm ParaSNPid.txt')

os.system(mainBox+'cp /data/{}.hg19_multianno.txt .'.format(num))

os.system(mainBox+'Rscript ParsSNP_application.r {}.hg19_multianno.txt'.format(num))


os.system(mainBox+'mv ParsSNP.output.{}.hg19_multianno.txt /data'.format(num))

os.system('mv ParsSNP.output.{}.hg19_multianno.txt {}.hg19_multianno.ParsSNP.output.txt'.format(num, num))

os.system('sudo docker rm -f {}'.format(mainID))
